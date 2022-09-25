# 예제 설명

필립스 휴 써드파티 디바이스를 통제할 수 있는 Thing 예제

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
    
    Hue 브릿지 ip 주소
    
- `-bp, --bridge_port | default=80`
    
    Hue 브릿지 port 번호
    
- `-k --user_key | default=''`
    
    사용자 API 키
    
- `-sc --scan_cycle | default=60`
    
    Hue 디바이스 스캔 주기
    
- `-md --mode | default=SoPManagerMode.SPLIT.value`
    
    Manager Thing 모드.
    
    1. `SoPManagerMode.SPLIT`
        
        Hue 디바이스가 별개의 Thing으로써 동작
        
    2. `SoPManagerMode.JOIN`
        
        Hue 디바이스가 한 개의 Thing으로 묶여서 동작
        

# Services

## Function Services

- `on(None) -> bool`
    
    Hue 디바이스를 켜는 서비스
    
- `off(None) -> bool`
    
    Hue 디바이스를 끄는 서비스
    
- `set_brightness(brightness: int) -> bool`
    
    Hue 디바이스의 밝기를 조정하는 서비스
    
- `set_color(r: int, g: int, b: int) -> bool`
    
    Hue 디바이스의 색을 조정하는 서비스
    
- `set_brightness(brightness: int) -> bool`
    
    Hue 디바이스의 밝기를 조정하는 서비스
    
- `set_brightness(brightness: int) -> bool`
    
    Hue 디바이스의 밝기를 조정하는 서비스
    

## Value Services

- (없음)