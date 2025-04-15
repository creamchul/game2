# 게임 UI에 적용할 CSS 스타일 정의

def get_game_style():
    return """
    <style>
    .main-title {
        color: #4B0082;
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .character-card {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s;
        height: 100%;
        margin-bottom: 1rem;
    }
    
    .character-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 8px rgba(0,0,0,0.2);
    }
    
    .character-title {
        color: #4B0082;
        text-align: center;
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .character-stats {
        color: #333;
        font-size: 1rem;
    }
    
    .ascii-art {
        font-family: monospace;
        white-space: pre;
        line-height: 1;
        font-size: 12px;
        color: #333;
        margin: 0 auto;
        text-align: center;
    }
    
    .floor-display {
        background-color: #4B0082;
        color: white;
        text-align: center;
        padding: 0.5rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    
    .player-stats {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .event-box {
        background-color: #fff8e1;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #ffd54f;
    }
    
    .message-box {
        background-color: #e8f5e9;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #66bb6a;
    }
    
    .door-container {
        display: flex;
        justify-content: space-around;
        margin: 1rem 0;
    }
    
    .item-button {
        background-color: #e3f2fd;
        border: 1px solid #bbdefb;
        padding: 0.5rem;
        border-radius: 5px;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        transition: background-color 0.3s;
    }
    
    .item-button:hover {
        background-color: #bbdefb;
    }
    
    .ultimate-button {
        background-color: #ffebee;
        border: 1px solid #ffcdd2;
        padding: 0.5rem;
        border-radius: 5px;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        transition: background-color 0.3s;
    }
    
    .ultimate-button:hover {
        background-color: #ffcdd2;
    }
    
    .stacked-column {
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    
    .door-box {
        border: 2px solid #4B0082;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .door-box:hover {
        background-color: #f0e6ff;
    }
    
    .emoji-large {
        font-size: 2rem;
    }
    
    .game-over {
        background-color: #ffebee;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 2rem;
    }
    
    .game-complete {
        background-color: #e8f5e9;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-top: 2rem;
    }
    </style>
    """ 