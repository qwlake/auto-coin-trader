# auto-coin-trader

본 프로그램은 비트코인의 가격을 예측하여 자동으로 비트코인 거래소 Poloniex에서 자동 매매를 하는 프로그램이다.

## Features

* 비트코인 거래소 [Poloniex](https://docs.poloniex.com/)에서 거래정보를 받아와 [TA-lib](https://mrjbq7.github.io/ta-lib/)에 넣어 수백 개의 기술 지표 값을 얻는다. 이를 통해 얻어진 값들을 유전 알고리즘에 적용시켰다. 
* 유전 알고리즘의 `적합도 함수`를 구성하는 방법은 각 지표들의 유사도를 이용했다. A 형태를 띄는 지표들의 집합을 두고, 시간의 순서대로 검사했을 때, 똑같이 A 형태를 보이는 경우가 있다면, 이 경우들을 저장한다. 이 경우가 해당 날로부터 가까운 미래에 가격이 상승하는 시점이 많다면, 이 A 형태를 보이는 지표들의 집합은 높은 적합도 함수를 가지는 것이다. 이와 같은 방식으로 적합도가 높은 지표들의 집합을 여러 세대에 걸쳐 찾아낸다. 

## Getting Started

### Prerequisites

```
python3
```

### Installing

windows:
1. [TA-lib](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib) 파일 다운로드
2. 다운로드 폴더로 이동 후 설치
```
cd "Your download folder"

# python3.6/64비트 사용시
pip install TA_Lib-0.4.10-cp36-cp36m-win_amd64.whl
pip install numpy matplotlib
```

Linux, mac:
```
pip install ta-lib
pip install numpy matplotlib
```


## Performance

![image](https://user-images.githubusercontent.com/41278416/82410456-e6788f80-9aaa-11ea-970a-f9f3f860e903.png)

![image](https://user-images.githubusercontent.com/41278416/82410499-fdb77d00-9aaa-11ea-8182-d04952d1f36d.png)
![image](https://user-images.githubusercontent.com/41278416/82410502-ff814080-9aaa-11ea-8195-cb8a1a4976f5.png)

100세대 동안 Train 데이터를 통해 학습시킨 결과, 세대가 지날수록 정확도가 증가하는 모습을 확인할 수 있다. 약 65프로의 정확도를 보인다.


## How it works

![image](https://user-images.githubusercontent.com/41278416/82409897-b5e42600-9aa9-11ea-8058-be51fe4f02d3.png)

▲임의의 유전자의 지표들의 집합 ( `A 형태`라고 가정 )



![제목 없음](https://user-images.githubusercontent.com/41278416/82410310-90a3e780-9aaa-11ea-8fae-386f9dcf744c.png)

▲순차대로 `A 형태`를 띄는 날이 있는지 탐색



![image](https://user-images.githubusercontent.com/41278416/82409941-ceecd700-9aa9-11ea-95af-4001b3910828.png)

▲ `A 형태`를 띄는 날로부터 가까운 시일 내에 가격이 N퍼센트 이상 상승하는 날이 있다면 적합도 증가



![image](https://user-images.githubusercontent.com/41278416/82409943-d01e0400-9aa9-11ea-910c-f3e2b55ff465.png)

▲ ①~⑩번을 N번(N세대) 반복한 후, ⑪,⑫번을 통해 결과 도출


## Limit and Improvement

지표의 수가 한정적이다 보니, 다양한 유전자를 구성하는 데에 제한적이고 세대를 반복하여도 더 이상 발전하지 않는 임계점이 빨리 찾아온다. 또한 OverFitting의 우려도 있다. 이는 지표들의 매개변수를 다양화하여 생성 가능한 유전자의 수를 늘리는 것이 해답 중 하나가 될 수 있을것이라고 생각한다. 
