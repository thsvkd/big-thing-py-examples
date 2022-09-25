# 예제 설명

사람을 감지하는 서비스를 제공하는 Thing 예제. 

# prerequirement

```
chmod +x preinstall.sh
./preinstall.sh
```

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
    
- `--log | default=True`
    
    Thing의 log기능의 활성화 여부. 
    

# Services

## Function Services

- (없음)

## Value Services

- `human_num -> int`
    
    현재 카메라에 잡힌 사람의 수를 제공하는 서비스