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
    st.session_state.items = []  # 아이템 목록
    st.session_state.ultimate_skill_used = False  # 궁극기 사용 여부
    st.session_state.event_active = False  # 이벤트 활성화 여부
    st.session_state.current_event = None  # 현재 이벤트
    st.session_state.ultimate_skill_active = False

# 캐릭터 선택 함수
def select_character(character):
    st.session_state.character_selected = True
    st.session_state.character = character
    st.session_state.game_started = True
    st.session_state.floor = 1
    st.session_state.items = []  # 아이템 초기화
    st.session_state.ultimate_skill_used = False  # 궁극기 사용 여부 초기화
    
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
    if st.session_state.event_active:
        return  # 이벤트가 활성화된 경우 문 선택 무시
    
    probabilities = st.session_state.door_probs
    good_door = st.session_state.good_door
    
    # 운 스탯 반영 (도적의 경우 운이 높아 확률 증가)
    luck_bonus = st.session_state.luck / 100
    if door == good_door:
        success_chance = probabilities[door] + luck_bonus
    else:
        success_chance = probabilities[door]  # 나쁜 문에는 운 보너스 미적용
    
    # 전사 궁극기: 함정 무시
    if st.session_state.character == "전사" and door != good_door and st.session_state.ultimate_skill_active:
        success_chance = 1.0
        st.session_state.ultimate_skill_active = False
        st.session_state.ultimate_skill_used = True
        st.session_state.message = "🛡️ 궁극기 발동! 함정을 무시했습니다!"
    
    # 도적 궁극기: 100% 도박 성공
    if st.session_state.character == "도적" and st.session_state.ultimate_skill_active:
        success_chance = 1.0
        st.session_state.ultimate_skill_active = False
        st.session_state.ultimate_skill_used = True
        st.session_state.message = "🎯 궁극기 발동! 100% 성공합니다!"
    
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
        return
    
    # 층수 확인
    if st.session_state.floor > 100:
        st.session_state.game_complete = True
        st.session_state.message = "🏆 축하합니다! 100층 던전을 모두 클리어했습니다!"
        return
    
    # 랜덤 이벤트 발생
    if random.random() < 0.3:  # 30% 확률로 이벤트 발생
        trigger_random_event()
    else:
        # 다음 층의 문 확률 설정
        setup_door_probabilities()

# 랜덤 이벤트 발생
def trigger_random_event():
    events = [
        "수상한 상자",
        "떠돌이 상인",
        "작은 샘",
        "보물 상자",
        "함정 방"
    ]
    
    event = random.choice(events)
    st.session_state.current_event = event
    st.session_state.event_active = True
    
    if event == "수상한 상자":
        st.session_state.event_description = "수상한 상자가 등장했습니다. 열어보시겠습니까?"
    elif event == "떠돌이 상인":
        st.session_state.event_description = "떠돌이 상인이 아이템을 팔고 있습니다. 구매하시겠습니까?"
    elif event == "작은 샘":
        st.session_state.event_description = "회복의 기운이 느껴지는 작은 샘이 있습니다. 물을 마시겠습니까?"
    elif event == "보물 상자":
        st.session_state.event_description = "반짝이는 보물 상자를 발견했습니다. 열어보시겠습니까?"
    elif event == "함정 방":
        st.session_state.event_description = "이 방은 함정으로 가득한 것 같습니다. 조심스럽게 통과하시겠습니까?"

# 이벤트 선택 처리
def handle_event_choice(choice):
    event = st.session_state.current_event
    result = ""
    
    if choice == "예":
        if event == "수상한 상자":
            if random.random() < 0.6:  # 60% 확률로 좋은 결과
                item = random.choice(["회복 물약", "사다리", "운 강화 부적"])
                st.session_state.items.append(item)
                result = f"🎁 상자에서 {item}을(를) 발견했습니다!"
            else:
                damage = random.randint(5, 15)
                st.session_state.hp -= damage
                result = f"💥 상자에서 함정이 작동했습니다! 체력 -{damage}"
        
        elif event == "떠돌이 상인":
            if st.session_state.gold >= 20:
                st.session_state.gold -= 20
                item = random.choice(["회복 물약", "사다리", "운 강화 부적"])
                st.session_state.items.append(item)
                result = f"🛒 {item}을(를) 구매했습니다. 금화 -20"
            else:
                result = "💰 금화가 부족합니다. 상인이 실망하며 떠났습니다."
        
        elif event == "작은 샘":
            heal = random.randint(15, 30)
            st.session_state.hp += heal
            result = f"💧 샘의 물을 마셨습니다. 체력 +{heal}"
        
        elif event == "보물 상자":
            gold_gain = random.randint(20, 50)
            st.session_state.gold += gold_gain
            result = f"💰 보물 상자에서 금화 {gold_gain}개를 발견했습니다!"
        
        elif event == "함정 방":
            if random.random() < 0.5:  # 50% 성공 확률
                item = random.choice(["회복 물약", "사다리", "운 강화 부적"])
                st.session_state.items.append(item)
                result = f"🏃 함정을 피해 무사히 통과했습니다! {item}을(를) 발견했습니다!"
            else:
                damage = random.randint(10, 20)
                st.session_state.hp -= damage
                result = f"💥 함정에 걸렸습니다! 체력 -{damage}"
    else:  # "아니오"
        result = "🚶 조심스럽게 그냥 지나갔습니다."
    
    st.session_state.message = result
    st.session_state.event_active = False
    
    # 체력 확인
    if st.session_state.hp <= 0:
        st.session_state.game_over = True
        st.session_state.message += "\n💀 체력이 0이 되었습니다. 게임 오버!"
        return
    
    # 다음 층의 문 확률 설정
    setup_door_probabilities()

# 아이템 사용 함수
def use_item(item_index):
    item = st.session_state.items[item_index]
    
    if item == "회복 물약":
        heal = random.randint(30, 50)
        st.session_state.hp += heal
        st.session_state.message = f"🧪 회복 물약을 사용했습니다. 체력 +{heal}"
    
    elif item == "사다리":
        st.session_state.floor += 1
        setup_door_probabilities()
        st.session_state.message = "🪜 사다리를 사용해 한 층을 건너뛰었습니다!"
    
    elif item == "운 강화 부적":
        luck_boost = random.randint(5, 10)
        st.session_state.luck += luck_boost
        st.session_state.message = f"🍀 운 강화 부적을 사용했습니다. 운 +{luck_boost}"
    
    # 아이템 제거
    st.session_state.items.pop(item_index)

# 궁극기 활성화 함수
def activate_ultimate():
    if not st.session_state.ultimate_skill_used:
        st.session_state.ultimate_skill_active = True
        st.session_state.message = "⚡ 궁극기가 활성화되었습니다! 다음 선택에 적용됩니다."
    else:
        st.session_state.message = "❌ 이미 궁극기를 사용했습니다."

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
    st.session_state.items = []
    st.session_state.ultimate_skill_used = False
    st.session_state.event_active = False
    st.session_state.ultimate_skill_active = False

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
        st.write("- 궁극기: 함정 무시 (1회)")
        st.button("전사 선택", on_click=select_character, args=("전사",))
    
    with col2:
        st.write("### 도적")
        st.write("- 체력: 100")
        st.write("- 운: 20")
        st.write("- 금화: 30")
        st.write("- 궁극기: 100% 성공 (1회)")
        st.button("도적 선택", on_click=select_character, args=("도적",))
    
    with col3:
        st.write("### 마법사")
        st.write("- 체력: 80")
        st.write("- 운: 10")
        st.write("- 금화: 10")
        st.write("- 특성: 문의 확률을 볼 수 있음")
        st.write("- 궁극기: 100% 확률 확인 (1회)")
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
    
    # 아이템 목록 표시
    if st.session_state.items:
        st.write("## 보유 아이템")
        for i, item in enumerate(st.session_state.items):
            st.button(f"{item} 사용", key=f"item_{i}", on_click=use_item, args=(i,))
    
    # 궁극기 버튼
    if not st.session_state.ultimate_skill_used:
        st.write("## 궁극기")
        if st.session_state.character == "전사":
            st.button("궁극기: 함정 무시", on_click=activate_ultimate)
        elif st.session_state.character == "도적":
            st.button("궁극기: 100% 성공", on_click=activate_ultimate)
        elif st.session_state.character == "마법사" and not st.session_state.ultimate_skill_used:
            # 마법사 궁극기는 즉시 발동 (100% 확률 확인)
            st.button("궁극기: 100% 확률 확인", on_click=lambda: 
                      st.session_state.update({
                          'ultimate_skill_used': True,
                          'message': "🔮 궁극기 발동! 다음 선택의 성공 확률이 100% 정확하게 보입니다!"
                      }))
    
    # 이벤트 활성화 확인
    if st.session_state.event_active:
        st.write(f"## 이벤트: {st.session_state.current_event}")
        st.write(st.session_state.event_description)
        col1, col2 = st.columns(2)
        with col1:
            st.button("예", on_click=handle_event_choice, args=("예",))
        with col2:
            st.button("아니오", on_click=handle_event_choice, args=("아니오",))
    # 일반 게임 진행
    else:
        st.write("## 두 개의 문이 보입니다. 어느 쪽을 선택하시겠습니까?")
        
        # 마법사인 경우 확률 표시
        if st.session_state.character == "마법사":
            # 궁극기 사용 중이면 100% 정확한 확률 표시
            if st.session_state.ultimate_skill_used and st.session_state.message == "🔮 궁극기 발동! 다음 선택의 성공 확률이 100% 정확하게 보입니다!":
                st.write(f"왼쪽 문 정확한 성공 확률: {st.session_state.door_probs['left']*100:.2f}%")
                st.write(f"오른쪽 문 정확한 성공 확률: {st.session_state.door_probs['right']*100:.2f}%")
                # 메시지 초기화
                st.session_state.message = "🔮 궁극기로 정확한 확률을 확인했습니다!"
            else:
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