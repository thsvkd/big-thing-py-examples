# 설명

이메일 전송 기능을 제공하는 Thing 예제

# 실행

```bash
cd big_thing/email_big_thing
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

- `send(receive_address:str, title:str, text: str) -> bool`
    
    `title`의 제목을 가지고 `text`입 의 본문을 가지는 이메일을 `receive_address`로 전송하는 서비스. 
    

## Value Services

- (없음)