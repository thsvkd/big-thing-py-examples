# 설명

이메일 전송 기능을 제공하는 Thing 예제

# 사전 준비

<aside>
💡 구글 이메일이 발신지 인경우 다음 앱 비밀번호 생성하여 해당 비밀번호를 기입해야한다

- 구글 앱 비밀번호 생성 방법
    1. [링크](https://myaccount.google.com/security)에서 앱 비밀번호 생성
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/d9a2ea0a-5a71-4416-9fb0-3c988a4eb32a/Untitled.png)
        
    2. `메일 - 기타(맞춤 이름)` 을 선택하여 생성
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/cb840f3a-81bc-41c6-b9eb-844efbbc73a9/Untitled.png)
        
        ![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/e52cc7c9-809f-49cb-ad66-3787f42a9f16/Untitled.png)
        
</aside>

---

발신 이메일 주소와 비밀번호를 `run.py`와 같은 디렉토리에 [secret.py](http://secret.py) 파일을 생성한 후 입력

```bash
SENDER_EMAIL = '****@gmail.com' # or '****@naver.com'

EMAIL_PASSWORD_GMAIL = '****'
EMAIL_PASSWORD_NAVER = '****'
EMAIL_PASSWORD_LIVE = '****'
```

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