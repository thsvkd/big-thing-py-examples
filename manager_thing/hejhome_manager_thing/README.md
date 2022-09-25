# 예제 설명

헤이홈 써드파티 디바이스를 통제할 수 있는 Thing 예제

# 실행

```bash
python run.py [options]
```

# 옵션

- `-n, --name | default = None`
    
    Thing의 이름. 이 이름은 Thing을 구분하기위한 ID이기도 하다 
    
- `-ip --host | default='127.0.0.1'`
    
    Thing의 ip 주소
    
- `-p, --port | default=1883`
    
    Thing의 port 번호
    
- `-ac, --alive_cycle | default=60`
    
    Thing의 alive 패킷 전송 주기. alive 패킷을 통해 Middleware가 Thing의 활성화 여부를 파악한다. 
    
- `-bip, --bridge_host | default='https://goqual.io/openapi'`
    
    Hejhome 클라우드 브릿지 ip 주소
    
- `-bp, --bridge_port | default=80`
    
    Hejhome 클라우드 브릿지 port 번호
    
- `-k --user_key | default=''`
    
    사용자 API 키
    
- `-sc --scan_cycle | default=60`
    
    Hejhome 디바이스 스캔 주기
    
- `-md --mode | default=SoPManagerMode.SPLIT.value`
    
    Manager Thing 모드.
    
    1. `SoPManagerMode.SPLIT`
        
        Hejhome 디바이스가 별개의 Thing으로써 동작
        
    2. `SoPManagerMode.JOIN`
        
        Hejhome 디바이스가 한 개의 Thing으로 묶여서 동작
        

# Services

## Function Services

- `on(None) -> bool`
    
    Hejhome 디바이스를 켜는 서비스
    
- `off(None) -> bool`
    
    Hejhome 디바이스를 끄는 서비스
    
- `curtain_open(None) -> bool`
    
    커튼 Hejhome 디바이스의 커튼을 여는 서비스
    
- `curtain_close(None) -> bool`
    
    커튼 Hejhome 디바이스의 커튼을 는 서비스
    
- `switch_set(index: int, on: bool) -> bool`
    
    zigbee Hejhome 스위치 디바이스의 전원을 조정하는 서비
    

## Value Services

- (없음)