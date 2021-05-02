import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from PIL import Image

# desired size of the output image, need to be 224,244 to use pretrained model
mean = [0.5734, 0.4586, 0.2882]
std = [0.2108, 0.2169, 0.1982]
img_size = 224, 224


def preprocess_image(pil_image):
    image_transforms = transforms.Compose([transforms.Resize(img_size),
                                           transforms.ToTensor(),
                                           transforms.Normalize(mean, std)])
    image_tensor = image_transforms(pil_image)
    # need to add one dimension, need to be 4D to pass into the network
    image_tensor.unsqueeze_(0)
    image_tensor.cpu()
    return image_tensor


def load_model():
    model = torchvision.models.resnet18(pretrained=True)
    for param in model.parameters():
        param.require = False
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, 2)
    model = model.cpu()
    model.load_state_dict(torch.load('net.pth', map_location='cpu'))
    return model


def get_prediction(model, image_tensor):
    model.eval()
    output = model(image_tensor)
    _, prediction = torch.max(output, dim=1)
    return bool(prediction)


def lets_rock(pil_image):
    model = load_model()
    image_tensor = preprocess_image(pil_image)
    prediction = get_prediction(model, image_tensor)
    return prediction
