# https://tutorials.pytorch.kr/beginner/blitz/cifar10_tutorial.html
# cifar-10 classification 
import torch
import torchvision 
import torchvision.transforms as transforms 
import matplotlib.pyplot as plt 
import numpy as np 
import torch.nn as nn 
import torch.nn.functional as F 
import torch.optim as optim

transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform = transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size = 4, shuffle = True, num_workers = 2)

testset = torchvision.datasets.CIFAR10(root='./data', train = False, download=True, transform = transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=4, shuffle=False, num_workers=2)

classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

'''
RuntimeError:... 
# 이미지를 보여주기 위한 함수
def imshow(img):
    img = img / 2 + 0.5
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()

#학습용 이미지를 무작위로 가져오기
dataiter = iter(trainloader)
images, labels = dataiter.next()

#이미지 보여주기
imshow(torchvision.utils.make_grid(images))
#정답(label)출력
print(' '.join('%5s' %classes[labels[j]] for j in range(4) ))
'''

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

        def forward(self, x):
            x = self.pool(F.relu(self.conv1(x)))
            x = self.pool(F.relu(self.conv2(x)))
            x = x.view(-1, 16 * 5 * 5)
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            x = self.fc3(x)
            return x 

net = Net()


criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr = 0.001, momentum=0.9)

for epoch in range(2):

    running_loss = 0.0
    for i , data in enumerate(trainloader, 0):
        #[input, labels]의 목록인 data로부터 입력을 받은 후
        inputs, labels = data 

        #변화도(Gradient) 매개변수를 0으로 만들고

        optimizer.zero_grad()

        #순전파 + 역전파 + 최적화를 한 후 
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        #통계를 출력
        running_loss += loss.item()
        if i % 2000 == 1999: # print every 2000 mini-batches
            print('[%d, %5d] loss: %3.f' %(epoch+1, i+1, running_loss / 2000))

print('Finished Training')

PATH = 'D:/program/python/torch/cifar_net.pth'
torch.save(net.sate_dict(), PATH)

#시험용 데이터로 신경망 검사하기 
dataiter = iter(testloader)
images, labels = dataiter.next()

#이미지를 출력
imshow(torchvision.utils.make_grid(images))
print('GroundTruth: ', ' '.join('%5s' %classes[labels[j]] for j in range(4) ))


