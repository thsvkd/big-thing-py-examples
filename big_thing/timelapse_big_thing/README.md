# 설명

일정시간마다 사진을 찍어 타임랩스 동영상을 만들 수 있는 Thing 예제

# 의존성

- Windows
    1. 필요한 python 모듈 설치
        
        ```bash
        pip install -r requirements.txt
        ```
        
- Mac
    1. 필요한 python 모듈 설치
        
        ```bash
        pip install -r requirements.txt
        ```
        
    2. 앱 실행시 다음과 같이 권한 부여 팝업이 뜹니다. 이 때 확인을 눌러 카메라 권한을 부여합니다. (***반드시 맥 GUI 환경에서 실행하여야 다음과 같은 팝업이 뜨니 원격접속대신 직접 맥북을 사용하시기 바랍니다.***)
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/0cf08f68-ddad-475d-a1f1-49555b7c1b01/Untitled.png)
        
- Raspberry Pi
    1. 필요한 라이브러리, python 모듈 설치
        
        ```bash
        sudo apt install libatlas-base-dev python3-dev -y
        pip install -r requirements.txt
        sudo raspi-config # Interface Options -> Legacy Camera -> Yes -> Ok -> Esc(quit)
        sudo reboot
        ```
        

### 카메라 설치

- Raspberry Pi
    1. 아래와 같은 Raspberry Pi용 카메로 모듈 준비
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e3c678cc-5177-4771-93fa-ac1b2b8b2ea7/Untitled.jpeg)
        
    2. Raspberry Pi와 결합
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/bbc8154a-64e2-4806-8b15-4bfd218f30fe/Untitled.png)
        
- 그 외 플랫폼
    1. 웹캠 준비
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/4c5c6f3f-6235-4cc2-a08d-353671872098/Untitled.png)
        
    2. 노트북의 경우 내장된 웹캠 사용 가능
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/1c19d156-ede9-4ad5-94c3-48ad96de9f75/Untitled.png)
        

# 실행

```bash
cd big_thing/timelapse_big_thing
python run.py
```

# 옵션

- `-n, --name | default = None`
    
    Thing의 이름. 이 이름은 Thing을 구분하기위한 ID이기도 하다 
    
- `-ip --host | default='127.0.0.1'`
    
    Thing의 ip 주소
    
- `-p, --port | default=11083`
    
    Thing의 port 번호
    
- `-ac, --alive_cycle | default=60`
    
    Thing의 alive 패킷 전송 주기. alive 패킷을 통해 Middleware가 Thing의 활성화 여부를 파악한다. 
    
- `-as, --auto_scan | default=True`
    
    Middleware 자동스캔 기능 활성화 여부.
    
- `--log | default=True`
    
    Thing의 log기능의 활성화 여부. 
    

# Services

## Function Services

- `timelapse_start(None) -> int`
    
    타입랩스 캡쳐를 시작하는 서비스
    
- `timelapse_stop(None) -> int`
    
    타입랩스 캡쳐를 중지하는 서비스
    
- `timelapse_makevideo(dst: str) -> int`
    
    캡쳐한 사진을 비디오로 변환하는 서비스. 변환에 성공하면 True를 반환한다.
    
    캡쳐한 이미지들은 기본적으로 `./capture_images` 에 저장되고, 변환된 동영상은 `dst`에 명세된 경로 에 저장됩니다. 
    

## Value Services

- (없음)