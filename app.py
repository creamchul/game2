import streamlit as st
import random

# 세션 상태 초기화
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.character_selected = False
    st.session_state.floor = 0
    st.session_state.hp = 0
    st.session_state.luck = 0
    st.session_state.gold = 0
    st.session_state.character = None
    st.session_state.game_over = False
    st.session_state.game_complete = False
    st.session_state.message = ""
    st.session_state.door_probs = {"left": 0.5, "right": 0.5}

# 캐릭터 선택 함수
def select_character(character):
    st.session_state.character_selected = True
    st.session_state.character = character
    st.session_state.game_started = True
    st.session_state.floor = 1
    
    if character == "전사":
        st.session_state.hp = 150
        st.session_state.luck = 5
        st.session_state.gold = 0
    elif character == "도적":
        st.session_state.hp = 100
        st.session_state.luck = 20
        st.session_state.gold = 30
    elif character == "마법사":
        st.session_state.hp = 80
        st.session_state.luck = 10
        st.session_state.gold = 10
    
    # 첫 층의 문 확률 설정
    setup_door_probabilities()

# 문 확률 설정
def setup_door_probabilities():
    left_prob = random.randint(30, 70) / 100
    right_prob = 1 - left_prob
    
    st.session_state.door_probs = {
        "left": left_prob,
        "right": right_prob
    }
    
    # 좋은 문 결정 (확률이 높은 문이 좋은 문)
    if left_prob > right_prob:
        st.session_state.good_door = "left"
    else:
        st.session_state.good_door = "right"

# 문 선택 처리 함수
def choose_door(door):
    probabilities = st.session_state.door_probs
    good_door = st.session_state.good_door
    
    # 운 스탯 반영 (도적의 경우 운이 높아 확률 증가)
    luck_bonus = st.session_state.luck / 100
    if door == good_door:
        success_chance = probabilities[door] + luck_bonus
    else:
        success_chance = probabilities[door] + luck_bonus
    
    # 문의 결과 결정
    if random.random() < success_chance:
        # 성공
        gold_gain = random.randint(10, 30 + st.session_state.floor)
        st.session_state.gold += gold_gain
        st.session_state.message = f"🎉 성공! 금화 +{gold_gain} 획득!"
    else:
        # 함정
        damage = random.randint(10, 15 + st.session_state.floor // 10)
        st.session_state.hp -= damage
        st.session_state.message = f"💥 함정에 빠졌습니다! 체력 -{damage}"
    
    # 다음 층으로 이동
    st.session_state.floor += 1
    
    # 체력 확인
    if st.session_state.hp <= 0:
        st.session_state.game_over = True
        st.session_state.message = "💀 체력이 0이 되었습니다. 게임 오버!"
    
    # 층수 확인
    if st.session_state.floor > 100:
        st.session_state.game_complete = True
        st.session_state.message = "🏆 축하합니다! 100층 던전을 모두 클리어했습니다!"
    else:
        # 다음 층의 문 확률 설정
        setup_door_probabilities()

# 게임 리셋
def reset_game():
    st.session_state.game_started = False
    st.session_state.character_selected = False
    st.session_state.floor = 0
    st.session_state.hp = 0
    st.session_state.luck = 0
    st.session_state.gold = 0
    st.session_state.character = None
    st.session_state.game_over = False
    st.session_state.game_complete = False
    st.session_state.message = ""

# UI 구성
st.title("텍스트 기반 로그라이크 던전 게임")

# 게임 시작 전 캐릭터 선택 화면
if not st.session_state.character_selected:
    st.write("던전에 입장할 캐릭터를 선택하세요:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("### 전사")
        st.write("- 체력: 150")
        st.write("- 운: 5")
        st.write("- 금화: 0")
        st.button("전사 선택", on_click=select_character, args=("전사",))
    
    with col2:
        st.write("### 도적")
        st.write("- 체력: 100")
        st.write("- 운: 20")
        st.write("- 금화: 30")
        st.button("도적 선택", on_click=select_character, args=("도적",))
    
    with col3:
        st.write("### 마법사")
        st.write("- 체력: 80")
        st.write("- 운: 10")
        st.write("- 금화: 10")
        st.write("- 특성: 문의 확률을 볼 수 있음")
        st.button("마법사 선택", on_click=select_character, args=("마법사",))

# 게임 진행 중이면 게임 화면 표시
elif st.session_state.game_started and not st.session_state.game_over and not st.session_state.game_complete:
    st.write(f"### {st.session_state.floor}층")
    
    # 플레이어 정보 표시
    st.write(f"## 플레이어 정보: {st.session_state.character}")
    col1, col2, col3 = st.columns(3)
    col1.metric("체력", st.session_state.hp)
    col2.metric("운", st.session_state.luck)
    col3.metric("금화", st.session_state.gold)
    
    # 메시지 표시
    if st.session_state.message:
        st.write(f"### {st.session_state.message}")
    
    st.write("## 두 개의 문이 보입니다. 어느 쪽을 선택하시겠습니까?")
    
    # 마법사인 경우 확률 표시
    if st.session_state.character == "마법사":
        st.write(f"왼쪽 문 성공 확률: {st.session_state.door_probs['left']*100:.0f}%")
        st.write(f"오른쪽 문 성공 확률: {st.session_state.door_probs['right']*100:.0f}%")
    
    # 선택 버튼
    col1, col2 = st.columns(2)
    with col1:
        st.button("왼쪽 문 선택", on_click=choose_door, args=("left",))
    with col2:
        st.button("오른쪽 문 선택", on_click=choose_door, args=("right",))

# 게임 오버
elif st.session_state.game_over:
    st.write("# 게임 오버!")
    st.write(f"## 당신은 {st.session_state.floor-1}층까지 도달했습니다.")
    st.write(f"## 획득한 금화: {st.session_state.gold}")
    st.button("다시 시작", on_click=reset_game)

# 게임 클리어
elif st.session_state.game_complete:
    st.write("# 축하합니다! 던전을 클리어했습니다!")
    st.write(f"## 최종 체력: {st.session_state.hp}")
    st.write(f"## 획득한 금화: {st.session_state.gold}")
    st.button("다시 시작", on_click=reset_game) 