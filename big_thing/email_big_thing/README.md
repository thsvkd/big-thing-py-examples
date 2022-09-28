# 설명

이메일 전송 기능을 제공하는 Thing 예제

# 의존성

```bash
pip install smtplib email
```

# 사전 준비

- 이메일 비밀번호 입력
    
    ```bash
    vi big_thing/email_big_thing/secret.py # 자신의 이메일 비밀번호를 기입
    ```
    

# 실행

```bash
cd big_thing/email_big_thing
pip install -r requirements.txt
python run.py [options]
```

# 옵션

- `-n, --name | default = None`
    
    Thing의 이름. 이 이름은 Thing을 구분하기 위한 ID이기도 하다 
    
- `-ip --host | default='127.0.0.1'`
    
    Thing의 ip 주소
    
- `-p, --port | default=1883`
    
    Thing의 port 번호
    
- `-ac, --alive_cycle | default=60`
    
    Thing의 alive 패킷 전송 주기. alive 패킷을 통해 Middleware가 Thing의 활성화 여부를 파악한다. 
    
- `-as, --auto_scan | default=True`
    
    Middleware 자동스캔 기능 활성화 여부.
    
- `--log | default=True`
    
    Thing의 log기능의 활성화 여부. 
    

# Services

## Function Services

- `email(address:str, text: str) -> bool`
    
    `text`를 입력으로 받아 `address` 의 이메일로 이메일을 전송한다. 
    

## Value Services

- (없음)