import streamlit as st
from PIL import Image
from datetime import datetime
import random

# --- 제목 ---
st.title("🧹 스마트 청소 관리 앱")

# --- 1단계: 이미지 업로드 ---
st.header(" 청소할 공간 사진 업로드")
uploaded_file = st.file_uploader("사진 선택", type=["jpg", "png", "jpeg"])
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드한 사진", use_column_width=True)
    st.success("사진 업로드 완료! (AI 공간 인식 기능은 여기서 처리됩니다)")

# --- 2단계: 청소할 공간 선택 ---
st.header(" 청소할 공간 선택")
areas = ["화장실", "주방", "거실", "침실", "욕실", "정원", "빨래"]
selected_area = st.selectbox("청소할 공간을 선택하세요:", areas)

# --- 3단계: 청소 작업 리스트 (체크박스) ---
st.header(" 청소 작업 목록")
tasks_dict = {
    "화장실": [
        "세면대와 거울 청소하기", "변기 청소하기", "바닥 쓸기", 
        "수납장 정리하기", "쓰레기통 청소하기", "화장지 교체하기", "개인용품 정리하기", 
        "창문 닦기", "탈취제 뿌리기", "샤워기 청소하기", "거울 선반 닦기", 
        "여분 용품 정리하기", "문 닦기", "사용한 물품 확인하기"
    ],
    "주방": [
        "설거지 하기", "바닥 쓸기", "바닥 닦기", "냉장고 정리", "가스레인지/인덕션 닦기", 
        "주방 상판 닦기", "서랍 정리", "그릇 닦기", "쓰레기 버리기", 
        "식탁 닦기", "건조식품 정리", "조미료 확인", "벽 닦기", "행주 교체", 
        "탈취제 뿌리기"
    ],
    # 다른 공간도 필요하면 추가
}

tasks = tasks_dict.get(selected_area, [])
st.subheader(f"✅ {selected_area} 청소 작업")
if tasks:
    for i, task in enumerate(tasks, 1):
        st.checkbox(f"{i}. {task}", key=f"{selected_area}_{i}")

# --- 4단계: 다음 청소 일정 설정 + 체크 알림 ---
st.header(" 다음 청소 일정 예약 및 알림")

# Lưu reminders vào session_state
if "reminders" not in st.session_state:
    st.session_state.reminders = []

next_clean_date = st.date_input("다음 청소 날짜 선택", datetime.now())
next_clean_time = st.time_input("다음 청소 시간 선택", datetime.now())
reminder_dt = datetime.combine(next_clean_date, next_clean_time)

if st.button("✅ 일정 저장"):
    st.session_state.reminders.append(reminder_dt)
    st.success(f"청소 일정 저장됨: {reminder_dt}")

# Nút kiểm tra nhắc nhở
if st.button("⏰ 체크 알림 확인"):
    now = datetime.now()
    if st.session_state.reminders:
        for r in st.session_state.reminders:
            if now >= r:
                st.warning(f"⏰ 지금은 청소할 시간이에요! (예정 시간: {r})")
            else:
                st.info(f"다음 청소 예정: {r}")
    else:
        st.info("저장된 청소 일정이 없습니다.")

# --- 5단계: 공간별 청소 팁/빠르게 끝내는 방법 ---
st.header(" 공간별 청소 팁")
tips_dict = {
    "화장실": [
        "큰 물건부터 정리하고 작은 것들을 닦으세요.",
        "세면대와 변기 주변은 하루에 한 번씩 빠르게 닦으세요.",
        "청소 도구를 미리 준비하면 시간을 절약할 수 있어요."
    ],
    "주방": [
        "조리대 위를 먼저 정리하고 설거지 후 바닥을 닦으세요.",
        "냉장고와 가스레인지는 주 1회 집중 청소하세요.",
        "쓰레기는 미리 버리고 필요한 도구만 꺼내세요."
    ],
    "거실": [
        "큰 가구 주변부터 청소하고 장식품 순서로 진행하세요.",
        "쿠션과 담요를 정리 후 바닥 청소를 하세요.",
        "카펫은 청소기로 빠르게 먼지를 제거하세요."
    ],
    "침실": [
        "침대 정리와 침구 교체부터 시작하세요.",
        "서랍과 옷장을 정리하면서 필요한 것만 남기세요.",
        "바닥 쓸기와 닦기를 마지막에 하세요."
    ],
    "욕실": [
        "샤워기, 세면대, 욕조 순으로 청소하세요.",
        "물청소는 마지막에 하여 물때를 최소화하세요.",
        "수건과 용품 정리는 빠르게 정리하세요."
    ],
    "정원": [
        "큰 잎과 낙엽을 먼저 제거하세요.",
        "식물 물주기와 잡초 제거를 병행하세요.",
        "도구는 미리 준비해 청소 시간을 줄이세요."
    ],
    "빨래": [
        "옷을 색상별로 분류한 후 세탁하세요.",
        "세탁 후 바로 널고 다림질 순으로 진행하세요.",
        "서랍 정리와 함께 옷 접기를 동시에 하면 효율적이에요."
    ]
}

st.subheader(f"💡 {selected_area} 청소 팁")
for i, tip in enumerate(tips_dict.get(selected_area, []), 1):
    st.checkbox(f"{i}. {tip}", key=f"{selected_area}_tip_{i}")

# --- 6단계: 완료 후 보상/칭찬 ---
st.header(" 청소 완료 🎁")

all_tasks_done = True
for i, task in enumerate(tasks, 1):
    if not st.session_state.get(f"{selected_area}_{i}", False):
        all_tasks_done = False
        break

if all_tasks_done and tasks:
    # Lời khen động lực
    praises = [
        "🌟 오늘도 청소 완료! 집이 반짝반짝 빛나요!",
        "💖 청소 미션 성공! 기분 좋은 하루가 될 거예요!",
        "🎊 훌륭해요! 깨끗한 공간에서 휴식하세요!",
        "🏡 모든 정리 끝! 편안하게 한숨 돌리세요!"
    ]
    st.success(random.choice(praises))
    # Câu thưởng cà phê
    st.info("☕ 커피 한 잔과 함께 오늘의 청소 성과를 감상해보세요!")
