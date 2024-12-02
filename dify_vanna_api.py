from fastapi import FastAPI, Body, HTTPException, Header  # 引入 FastAPI、Body、HTTPException 和 Header 模組
from pydantic import BaseModel  # 引入 Pydantic 的 BaseModel，用於數據驗證

# 載入Vanna套件
from vanna.ollama import Ollama
from vanna.chromadb import ChromaDB_VectorStore

# 定義數據庫和Vanna接口
class MyVanna(ChromaDB_VectorStore, Ollama):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        Ollama.__init__(self, config=config)
        
app = FastAPI()  # 建立 FastAPI 應用程式實例    

class InputData(BaseModel):  # 定義一個 Pydantic 的數據模型
    point: str  # 接收一個字符串類型的變數 'point'
    params: dict = {}  # 接收一個字典類型的變數 'params'，默認值為空字典

@app.post("/api/dify/receive")  # 定義 POST 路由 '/api/dify/receive'
async def dify_receive(data: InputData = Body(...), authorization: str = Header(None)):
    """接收 Dify 的 API 請求數據。"""
    expected_api_key = "123456"  # TODO: 你的 API 金鑰
    auth_scheme, _, api_key = authorization.partition(' ')  # 將 authorization 標頭拆分為認證模式和 API 金鑰

    if auth_scheme.lower() != "bearer" or api_key != expected_api_key:  # 驗證 Bearer 認證模式和 API 金鑰是否正確
        raise HTTPException(status_code=401, detail="Unauthorized")  # 驗證失敗時，回應 401 未授權

    point = data.point  # 獲取請求數據中的 'point'

    # 用於除錯，打印 'point'
    print(f"point: {point}")

    if point == "ping":  # 如果 'point' 是 'ping'
        return {
            "result": "pong"  # 回應 'pong'
        }
    if point == "app.external_data_tool.query":  # 如果 'point' 是 'app.external_data_tool.query'
        return handle_app_external_data_tool_query(params=data.params)  # 調用外部數據工具查詢的處理函數
    # elif point == "{point name}":
        # TODO: 在此處實現其他 'point' 的處理

    raise HTTPException(status_code=400, detail="Not implemented")  # 如果 'point' 不被支持，回應 400 錯誤    
    
def handle_app_external_data_tool_query(params: dict):  # 處理外部數據工具查詢的函數
    app_id = params.get("app_id")  # 從參數中取得 'app_id'
    tool_variable = params.get("tool_variable")  # 從參數中取得 'tool_variable'
    inputs = params.get("inputs")  # 從參數中取得 'inputs'
    query = params.get("query")  # 從參數中取得 'query'

    
    # 創建 MyVanna 實例
    vn = MyVanna(config={'model': 'mistral'})
        
    documentation = '''
    SEASON_1 & SEASON_2: Season indicator variables
    TEAM_ID: NBA's unique ID variable of that specific team in their API.
    PLAYER_ID: NBA's unique ID variable of that specific player in their API.
    PLAYER_NAME: Name of the player.
    GAME_DATE: Date of the game (M-D-Y // Month-Date-Year).
    GAME_ID: NBA's unique ID variable of that specific game in their API.
    EVENT_TYPE: Character variable denoting a shot outcome (Made Shot // Missed Shot).
    SHOT_MADE: variable denoting a shot outcome (1 // 0).
    ACTION_TYPE: Description of shot type (layup, dunk, jump shot, etc.).
    SHOT_TYPE: Type of shot (2PT or 3PT).
    BASIC_ZONE: Name of the court zone the shot took place in.
    Restricted Area, In the Paint (non-RA), Midrange, Left Corner 3, Right Corner 3, Above the Break, Backcourt.
    ZONE_NAME: Name of the side of court the shot took place in.
    left, left side center, center, right side center, right
    ZONE_ABB: Abbreviation of the side of court.
    (L), (LC), (C), (RC), (R).
    ZONE_RANGE: Distance range of shot by zones.
    Less than 8 ft., 8-16 ft. 16-24 ft. 24+ ft.
    LOC_X: X coordinate of the shot in the x, y plane of the court (0, 50).
    LOC_Y: Y coordinate of the shot in the x, y plane of the court (0, 50).
    SHOT_DISTANCE: Distance of the shot with respect to the center of the hoop, in feet.
    QUARTER: Quarter of the game.
    MINS_LEFT: Minutes remaining in the quarter.
    SECS_LEFT: Seconds remaining in minute of the quarter.
    '''

    vn.train(documentation=f"Please refer to the following content to understand the meaning of all the columns in the source of truth. {documentation}")

    # 連接到指定的數據庫
    try:
        vn.connect_to_sqlite('nba_shots.db')
    except Exception as e:
        return {"error": f"Database connection failed: {str(e)}"}
    
    # 生成 SQL 查詢
    try:
        sql_query = vn.generate_sql(query).strip().rstrip('[')  # 清理多餘的字符
        #print(f"sql_query: {sql_query}")
    except Exception as e:
        return {"error": f"Failed to generate SQL: {str(e)}"}
    
    # 執行 SQL 查詢
    try:
        if vn.is_sql_valid(sql_query): #先判斷是不是正常的sql語法
            df = vn.run_sql(sql_query)
            # 將結果轉換為 JSON 格式
            result = df.to_markdown(index=False) 
            print(f"query2: {result}")
        
        else:
            #有可能是問其它非數據分析的問題，就直接將一般生成的LLM結果回傳
            result = sql_query
            
        if not result:
            result = "查不到相關資料，請重新提問！"
        
    except Exception as e:
        return {"error": f"Failed to execute SQL: {str(e)}"}
    
    return {
            "result": result  # 回應結果
    }    
    
