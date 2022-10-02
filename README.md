# Bara LS

## Test 서버 주소

[https://8000.taewonkim.com](https://8000.taewonkim.com)

---

## 개발 환경 통일

### Python

---

#### Python version

- Python 3.8.10

#### venv

- python3.8-venv

```bash
sudo apt install python3.8-venv
```

- 사용법

```bash
# 프로젝트 폴더에서
python3 -m venv {가상환경 명칭}

# e.g.
python3 -m venv bara-ls-venv

# 근데 일반적으로 가상 환경 명칭 그냥 venv로 함
# e.g.
python3 -m venv venv

# activate 방법
source {path_to_venv}/bin/activate

# e.g.
source ./venv/bin/activate

# deactivate 방법
deactivate
```

- requirements 관련

```bash
# requirements 만들기 (가상환경 activate 상태라고 가정)
pip freeze > requirements.txt

# requirements 설치하기 (가상환경 activate 상태라고 가정)
pip install -r requirements.txt
```

#### Linter

- flake8

```bash
pip3 install flake8
```

#### Formatter

- black

```bash
pip3 install black
```

#### pip3 오류 발생 시

```bash
sudo apt install python3-pip
```

#### vscode

**Python extension 설치되어 있어야 함**

```
Ctrl + Shift + P
Open Settings(JSON)
```

```
"python.pythonPath": "/usr/bin/",
"python.defaultInterpreterPath": "/usr/bin/python3",
"python.linting.enabled": true,
"python.linting.pylintEnabled": false,
"python.linting.flake8Enabled": true,
"python.linting.flake8Args": ["--max-line-length=120"],
"python.formatting.provider": "black",
"python.formatting.blackPath": "/home/ktw/.local/lib/python3.8/site-packages/black",
"python.formatting.blackArgs": ["--line-length=120"],
"[python]": {
"editor.formatOnSave": true,
"editor.defaultFormatter": null,
"editor.tabSize": 4
},
```

python.formatting.blackPath 경로는 본인 파이썬 설치 경로에 맞게 수정할 것<br>
아마 높은 확률로 `"/home/ktw/.local/lib/python3.8/site-packages/black"` 에서<br>
**ktw** 부분만 본인 리눅스 계정명으로 변경하면 될거임

만약 python extension이 venv를 인식하지 못해 import 문 오류가 linting 된다면<br>
python.pythonPath 와 python.defaultInterpreterPath 를 수정해야 함

e.g.

```
"python.pythonPath": "/home/ktw/workspaces/warmemo/venv/bin/",
"python.defaultInterpreterPath": "/home/ktw/workspaces/warmemo/venv/bin/python3",
```

만약 그렇게 했다면 black과 flake8 또한 venv에 설치해줘야 linting과 formatting이 작동함

```bash
# venv 환경을 activate 했다고 가정
# source /{path_to_venv}/bin/activate

pip install flake8 black
```

### Docker / Docker-compose

---

#### Docker 설치 (Ubuntu 기준)

**root 계정이 아닌 user 계정에서 작업할 것**

```bash
sudo apt update
sudo apt install apt-transport-https ca-certificates curl gnupg-agent software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
"deb [arch=amd64] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) \
stable"
sudo apt update && sudo apt install docker-ce docker-ce-cli containerd.io -y
sudo docker -v
sudo systemctl enable docker
sudo systemctl status docker

sudo usermod -aG docker $USER
```

#### Docker-compose 설치

**root 계정이 아닌 user 계정에서 작업할 것**<br>
**docker를 먼저 설치하고 docker-compose 설치할 것**

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
sudo docker-compose -version
```
