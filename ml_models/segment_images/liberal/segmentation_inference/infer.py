from modeling.deeplab import *
import torch
from torch.autograd import Variable
from torchvision import transforms
from utils import create_sidewalk_segment, ImageFolderWithPaths
from tqdm import tqdm

DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
IMAGES_TO_SEGMENT_PATH = './data/'

deeplab_model = DeepLab(num_classes=2,
                backbone='xception').to(DEVICE)

print("Loaded Model")

# Apply pretrained deeplab weights
deeplab_model.load_state_dict(
    torch.load(
        './checkpoint.pth.tar'
    )['state_dict']
)

print("Loaded Best Trained Model")

# Create evaluation set
transform = transforms.Compose([
    transforms.Resize((1024, 2048)),
    transforms.ToTensor(),
])

evalset = ImageFolderWithPaths(IMAGES_TO_SEGMENT_PATH, transform=transform)
# dataset must be a multiple of 2
evalloader = torch.utils.data.DataLoader(evalset, batch_size=2, shuffle=False, num_workers=2)

print("Loaded Data")

# Make predictions
preds_list = []
imgs_list = []

with torch.no_grad():
    for loaded in tqdm(evalloader):
        imgs = loaded[0].to(DEVICE)
        preds = deeplab_model(imgs)

        create_sidewalk_segment(preds, imgs, './outputs/')

        del imgs
        del preds