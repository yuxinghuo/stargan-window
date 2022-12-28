from os.path import join as ospj

import torchvision.utils as vutils
from torch.utils import data
from torchvision import transforms
from torchvision.datasets import ImageFolder

from core.model import *

# 随机获取源图片和参考图片
class InputFetcher1:
    def __init__(self, loader, latent_dim=16):
        self.loader = loader
        self.latent_dim = latent_dim
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def _fetch_inputs(self):
        try:
            x, y = next(self.iter)
        except (AttributeError, StopIteration):
            self.iter = iter(self.loader)
            x, y = next(self.iter)
        return x, y

    def _fetch_refs(self):
        try:
            x, x2, y = next(self.iter_ref)
        except (AttributeError, StopIteration):
            self.iter_ref = iter(self.loader_ref)
            x, x2, y = next(self.iter_ref)
        return x, x2, y

    def __next__(self):
        x, y = self._fetch_inputs()
        inputs = Munch(x=x, y=y)
        return Munch({k: v.to(self.device)
                      for k, v in inputs.items()})


def get_test_loader(root, img_size=256, batch_size=32, num_workers=4):
    print('Preparing DataLoader for the generation phase...')
    transform = transforms.Compose([
        transforms.Resize([img_size, img_size]),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5],
                             std=[0.5, 0.5, 0.5]),
    ])
    dataset = ImageFolder(root, transform)
    return data.DataLoader(dataset=dataset,
                           batch_size=batch_size,
                           shuffle=False,
                           num_workers=num_workers,
                           pin_memory=True)


# 构建模型
def build_model(img_size, style_dim, w_hpf, num_domains, wing_path):
    generator = nn.DataParallel(Generator(img_size, style_dim, w_hpf=w_hpf))
    style_encoder = nn.DataParallel(StyleEncoder(img_size, style_dim, num_domains))
    generator_ema = copy.deepcopy(generator)
    style_encoder_ema = copy.deepcopy(style_encoder)
    nets_ema = Munch(generator=generator_ema, style_encoder=style_encoder_ema)
    if w_hpf > 0:
        fan = nn.DataParallel(FAN(fname_pretrained=wing_path).eval())
        fan.get_heatmap = fan.module.get_heatmap
        nets_ema.fan = fan

    return nets_ema


@torch.no_grad()
def sample(domain):
    # 参考图 需要考虑分域
    if domain == 'female' or domain == 'male':
        w_hpf = 1
        num_domains = 2
        modelName = './model/celeba_model.ckpt'
        src_dir = './src'
        ref_dir = './ref/celeba'
    elif domain == 'cat' or domain == 'dog' or domain == 'wild':
        w_hpf = 0
        num_domains = 3
        modelName = './model/afhq_model.ckpt'
        src_dir = './src'
        ref_dir = './ref/afhq'
    else:
        w_hpf = 1
        num_domains = 1
        modelName = './model/cartoon_model.ckpt'
        src_dir = './src'
        ref_dir = './ref/other'
    # 参数
    checkpoint_dir = './model/'
    result_dir = './result/'
    val_batch_size = 8
    img_size = 256
    latent_dim = 16
    style_dim = 64
    wing_path = './core/wing.ckpt'
    # resume_iter = 100000
    # 构建模型
    nets_ema = build_model(img_size, style_dim, w_hpf, num_domains, wing_path)
    # 加载训练好的模型
    print('Loading checkpoint from %s...' % modelName)
    module_dict = torch.load(modelName, map_location=torch.device('cpu'))
    for name, module in nets_ema.items():
        module.module.load_state_dict(module_dict[name], False)

    loaders = Munch(src=get_test_loader(root=src_dir,
                                        img_size=img_size,
                                        batch_size=val_batch_size),
                    ref=get_test_loader(root=ref_dir,
                                        img_size=img_size,
                                        batch_size=val_batch_size))
    src = next(InputFetcher1(loaders.src, latent_dim))
    ref = next(InputFetcher1(loaders.ref, latent_dim))
    resultFileName = ospj(result_dir, 'reference.jpg')
    print('Working on {}...'.format(resultFileName))
    # 翻译图片使用参考图
    N, C, H, W = src.x.size()
    wb = torch.ones(1, C, H, W).to(src.x.device)
    x_src_with_wb = torch.cat([wb, src.x], dim=0)
    masks = nets_ema.fan.get_heatmap(src.x) if w_hpf > 0 else None
    s_ref = nets_ema.style_encoder(ref.x, ref.y)
    s_ref_list = s_ref.unsqueeze(1).repeat(1, N, 1)
    # 去除第一行
    x_concat = [x_src_with_wb]
    # x_concat = []
    for i, s_ref in enumerate(s_ref_list):
        x_fake = nets_ema.generator(src.x, s_ref, masks=masks)
        x_fake_with_ref = torch.cat([x_fake], dim=0)
        # 去除第一列
        x_fake_with_ref = torch.cat([ref.x[i:i + 1], x_fake], dim=0)
        x_concat += [x_fake_with_ref]
    x_concat = torch.cat(x_concat, dim=0)
    # 保存图片
    x = ((x_concat + 1) / 2).clamp_(0, 1)  # 使非规范化
    vutils.save_image(x.cpu(), resultFileName, nrow=N + 1, padding=0)
    del x_concat


if __name__ == '__main__':
    # sample("female")
    # sample("cat")
    # sample("dog")
    # sample("mild")
    # sample("cartoon")
    sample("female")
