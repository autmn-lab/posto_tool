# Model 1: x ∈ [-15,15], y ∈ [-12,12], z ∈ [-15,15]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model1.lg --init="[[-2,1],[-1.6,0.8],[-2.4,1.2]]" --timestamp=80 --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model1.json --prob=1 --dtlog=0.1
    
python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model1.lg --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model1.json

# Model 2: theta1/theta2 ∈ [-3,3], omega1/omega2 ∈ [-6,6]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model2.lg --init="[[0,0.8],[0,0.8],[0,2],[0,2]]" --timestamp=80 --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model2.json --prob=1 --dtlog=0.1
    
python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model2.lg --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model2.json

# Model 3: prey ∈ [-10,250], pred ∈ [-10,150], env ∈ [-60,60]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model3.lg   --init="[[12.25,31.85],[52.08,54.83],[-17.47,-14.23]]" --timestamp=60   --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model3.json --prob=1 --dtlog=0.1

python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model3.lg \
    --mode=equation --model_path=/home/prachi-bhattacharjee/Posto/models/model3.json

# Model 4: room1–room3 ∈ [0,40], heater ∈ [-5,6], load ∈ [-9,9]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model4.lg --init="[[20,23],[20,23],[20,23],[2.5,3.25],[0,2.4]]" --timestamp=100 --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model4.json --prob=1 --dtlog=0.1
    
python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model4.lg  --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model4.json

# Model 5: inventory ∈ [-20,220], production ∈ [-10,110], demand ∈ [-20,60], backlog ∈ [-20,60]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model5.lg --init="[[68.87,88.87],[0,19.73],[4.72,13.72],[-10,-0.54]]" --timestamp=80 --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model5.json --prob=1 --dtlog=0.1
    
python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model5.lg \
    --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model5.json

# Model 6: V ∈ [-20,20], I ∈ [-8,8], T ∈ [-15,60]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model6.lg --init="[[3.05,7.55],[-0.99,0.01],[-8.82,3.18]]" --timestamp=60 --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model6.json --prob=1 --dtlog=0.1
    
python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model6.lg  --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model6.json

# Model 7: q1–q5 ∈ [-3,3]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model7.lg --init="[[-1.77,-1.17],[-0.59,0.21],[0.17,0.97],[0.78,1.18],[1.25,2.00]]" --timestamp=60 --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model7.json --prob=1 --dtlog=0.1


python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model7.lg \
    --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model7.json

# Model 8: A,B ∈ [-20,120], C,D ∈ [-15,65]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model8.lg --init="[[-4.5,6.5],[-4.5,6.5],[-7,-1],[-7,-1]]" --timestamp=60 --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model8.json --prob=1 --dtlog=0.1
    
python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model8.lg \
    --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model8.json

# Model 9: price ∈ [-10,310], trend ∈ [-60,60], vol ∈ [-5,15], shock ∈ [-60,60]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model9.lg --init="[[175.12,235.12],[34.79,50.0],[3.31,3.81],[-26.27,-21.27]]" --timestamp=60 --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model9.json --prob=1 --dtlog=0.1
    
python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model9.lg --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model9.json

# Model 10: p ∈ [-25,25], q ∈ [-20,20], r ∈ [-22,22], s ∈ [-15,15]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model10.lg --init="[[-4.23,-2.23],[0.44,6.44],[-6.47,-4.67],[3.71,4.91]]" --timestamp=60 --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model10.json --prob=1 --dtlog=0.1
    
python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model11.lg \
    --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model11.json

