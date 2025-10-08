# Model 1: x ∈ [-15,15], y ∈ [-12,12], z ∈ [-15,15]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model1.lg \
    --init="[[-15,15],[-12,12],[-15,15]]" --timestamp=1000 --mode="equation" \
    --model_path=/home/prachi-bhattacharjee/Posto/models/model1.json --prob=1 --dtlog=0.1
    
python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model1.lg \
    --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model1.json

# Model 2: theta1/theta2 ∈ [-3,3], omega1/omega2 ∈ [-6,6]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model2.lg \
    --init="[[-3,3],[-3,3],[-6,6],[-6,6]]" --timestamp=1000 --mode="equation" \
    --model_path=/home/prachi-bhattacharjee/Posto/models/model2.json --prob=1 --dtlog=0.1
    
python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model2.lg \
    --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model2.json

# Model 3: prey ∈ [-10,250], pred ∈ [-10,150], env ∈ [-60,60]
# Model 3: Start in a range well below the upper bounds, then generate logs sparsely
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model3.lg \
    --init="[[50,150],[10,50],[-20,20]]" --timestamp=1000 --mode="equation" \
    --model_path=/home/prachi-bhattacharjee/Posto/models/model3.json --prob=1 --dtlog=0.1

python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model3.lg \
    --mode=equation --model_path=/home/prachi-bhattacharjee/Posto/models/model3.json

# Model 4: room1–room3 ∈ [0,40], heater ∈ [-5,6], load ∈ [-9,9]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model4.lg \
    --init="[[0,40],[0,40],[0,40],[-5,6],[-9,9]]" --timestamp=1000 --mode="equation" \
    --model_path=/home/prachi-bhattacharjee/Posto/models/model4.json --prob=1 --dtlog=0.1
    
python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model4.lg \
    --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model4.json

# Model 5: inventory ∈ [-20,220], production ∈ [-10,110], demand ∈ [-20,60], backlog ∈ [-20,60]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model5.lg \
    --init="[[-20,220],[-10,110],[-20,60],[-20,60]]" --timestamp=1000 --mode="equation" \
    --model_path=/home/prachi-bhattacharjee/Posto/models/model5.json --prob=1 --dtlog=0.1
    
python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model5.lg \
    --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model5.json

# Model 6: V ∈ [-20,20], I ∈ [-8,8], T ∈ [-15,60]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model6.lg \
    --init="[[-20,20],[-8,8],[-15,60]]" --timestamp=1000 --mode="equation" \
    --model_path=/home/prachi-bhattacharjee/Posto/models/model6.json --prob=1 --dtlog=0.1
    
python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model6.lg \
    --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model6.json

# Model 7: q1–q5 ∈ [-3,3]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model7.lg \
    --init="[[-3,3],[-3,3],[-3,3],[-3,3],[-3,3]]" --timestamp=1000 --mode="equation" \
    --model_path=/home/prachi-bhattacharjee/Posto/models/model7.json --prob=1 --dtlog=0.1
    
python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model7.lg \
    --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model7.json

# Model 8: A,B ∈ [-20,120], C,D ∈ [-15,65]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model8.lg \
    --init="[[-20,120],[-20,120],[-15,65],[-15,65]]" --timestamp=1000 --mode="equation" \
    --model_path=/home/prachi-bhattacharjee/Posto/models/model8.json --prob=1 --dtlog=0.1
    
python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model8.lg \
    --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model8.json

# Model 9: S,R ∈ [-100,1100], E,I,V ∈ [-50,550]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model9.lg \
    --init="[[-100,1100],[-50,550],[-50,550],[-100,1100],[-50,550]]" --timestamp=1000 --mode="equation" \
    --model_path=/home/prachi-bhattacharjee/Posto/models/model9.json --prob=1 --dtlog=0.1
    
python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model9.lg \
    --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model9.json

# Model 10: price ∈ [-10,310], trend ∈ [-60,60], vol ∈ [-5,15], shock ∈ [-60,60]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model10.lg \
    --init="[[-10,310],[-60,60],[-5,15],[-60,60]]" --timestamp=1000 --mode="equation" \
    --model_path=/home/prachi-bhattacharjee/Posto/models/model10.json --prob=1 --dtlog=0.1
    
python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model10.lg \
    --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model10.json

# Model 11: p ∈ [-25,25], q ∈ [-20,20], r ∈ [-22,22], s ∈ [-15,15]
python3 posto.py generateLog --log=/home/prachi-bhattacharjee/Posto/logs/model11.lg \
    --init="[[-25,25],[-20,20],[-22,22],[-15,15]]" --timestamp=1000 --mode="equation" \
    --model_path=/home/prachi-bhattacharjee/Posto/models/model11.json --prob=1 --dtlog=0.1
    
python3 posto.py checkSafety --log=/home/prachi-bhattacharjee/Posto/logs/model11.lg \
    --mode="equation" --model_path=/home/prachi-bhattacharjee/Posto/models/model11.json

