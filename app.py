import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import cv2

# ==========================================
# 1. 页面基础配置与全局状态初始化
# ==========================================
st.set_page_config(
    page_title="大型水库大坝安全 AI 辅助管理系统",import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import cv2

# ==========================================
# 1. 页面基础配置与全局状态初始化
# ==========================================
st.set_page_config(
    page_title="大型水库大坝安全 AI 辅助管理系统",
    page_icon="🌊",
    layout="wide"
)

# 使用 Streamlit 的 session_state 来记录和保持用户点击的验证状态
if 'iot_anomaly' not in st.session_state:
    st.session_state.iot_anomaly = False
if 'cv_alert' not in st.session_state:
    st.session_state.cv_alert = False

st.title("🌊 大型水库大坝安全 AI 辅助管理程序原型 (全兼容版本)")
st.markdown("---")

# ==========================================
# 2. 侧边栏：系统控制与动态验证沙箱
# ==========================================
st.sidebar.header("⚙️ 系统控制面板")
st.sidebar.subheader("当前监控大坝：高峡水库主坝")

# 模拟 AI 运行状态
ai_status = st.sidebar.selectbox("AI 算法引擎状态", ["正常运行", "算法维护", "离线异常"])
if ai_status == "正常运行":
    st.sidebar.success("🤖 AI 核心引擎已就绪")
else:
    st.sidebar.error("⚠️ AI 引擎未正常工作")

st.sidebar.markdown("---")

# 🧪 互动测试沙箱
st.sidebar.header("🧪 动态验证沙箱 (测试用)")
st.sidebar.markdown("你可以通过以下按钮，手动制造大坝险情，验证 AI 的实时响应能力：")

# 验证控制 1：模拟物联网故障发生
if st.sidebar.button("💥 注入大坝渗流异常数据", type="secondary", key="btn_iot_anomaly"):
    st.session_state.iot_anomaly = True
    st.toast("已成功注入管涌异常数据！请查看 IoT 标签页", icon="📈")

# 验证控制 2：模拟视觉红线越界发生
if st.sidebar.button("🚶 模拟社会人员越界触发红线", type="secondary", key="btn_cv_alert"):
    st.session_state.cv_alert = True
    st.toast("已触发电子红线入侵警报！请查看 CV 标签页", icon="👁️")

# 重置验证按钮
if st.sidebar.button("🔄 恢复系统至安全状态", type="primary", key="btn_reset_all"):
    st.session_state.iot_anomaly = False
    st.session_state.cv_alert = False
    st.toast("系统已重置，全部指标恢复正常安全水平。", icon="✅")

st.sidebar.markdown("---")
st.sidebar.info("""
**设计说明**：本程序严格遵循课程设计任务书要求，融合了物联网（IoT）时序预测与计算机视觉（CV）技术，实现大坝防汛与作业安全的智能化管控。
""")

# ==========================================
# 3. 核心功能划分（Tabs 标签页）
# ==========================================
tab1, tab2, tab3 = st.tabs(["📊 IoT 大坝结构渗流监测 (时序预测)", "👁️ CV 视频全时空监控 (行为识别)", "🚨 AI 智能应急指挥中心"])

# ------------------------------------------
# Tab 1: IoT 大坝结构渗流监测
# ------------------------------------------
with tab1:
    st.header("📈 基于 LSTM 算法的渗流与位移失稳预警")
    st.caption("利用物联网传感器收集渗压、水位数据，AI 预测未来48小时走势，实现隐患早发现。")
    
    # 动态数据发生器：根据侧边栏是否注入异常，改变生成的数学模型
    np.random.seed(42)
    time_axis = np.arange(-24, 48)
    
    if st.session_state.iot_anomaly:
        # 🚨 异常状态：AI 预测曲线呈现急剧指数级上升（模拟管涌）
        actual_data = np.concatenate([np.random.normal(5, 0.2, 25), [np.nan]*47])
        predict_data = np.concatenate([[np.nan]*24, [5.0], np.cumsum(np.random.uniform(0.1, 0.6, 47)) + 5])
    else:
        # ✅ 安全状态：AI 预测曲线在正常范围内平稳波动
        actual_data = np.concatenate([np.random.normal(5, 0.2, 25), [np.nan]*47])
        predict_data = np.concatenate([[np.nan]*24, [5.0], np.random.normal(5, 0.25, 47)])
        
    chart_data = pd.DataFrame({
        '时间 (小时后)': time_axis,
        '实际观测值 (mm)': actual_data,
        'AI 预测走势 (mm)': predict_data
    })
    
    # 使用 Plotly 绘制动态预测曲线
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=chart_data['时间 (小时后)'], y=chart_data['实际观测值 (mm)'], name='过去24小时实际渗流量', mode='lines+markers', line=dict(color='blue')))
    
    if st.session_state.iot_anomaly:
        fig.add_trace(go.Scatter(x=chart_data['时间 (小时后)'], y=chart_data['AI 预测走势 (mm)'], name='AI 预警：渗流指数级恶化 (存在管涌风险)', mode='lines', line=dict(color='red', dash='dash')))
    else:
        fig.add_trace(go.Scatter(x=chart_data['时间 (小时后)'], y=chart_data['AI 预测走势 (mm)'], name='AI 预测：未来48小时运行平稳', mode='lines', line=dict(color='green', dash='dash')))
        
    fig.update_layout(title="大坝背水坡 AP-03 测点渗流量实时预测图", xaxis_title="时间轴 (当前为 0 时刻)", yaxis_title="渗流量 (mm/d)")
    st.plotly_chart(fig, use_container_width=True, key="plotly_iot_chart")
    
    # 动态简报框展现
    if st.session_state.iot_anomaly:
        st.warning("⚠️ **AI 深度学习引擎预警简报**：监测到 AP-03 测点虽然当前数据（5.0mm）尚未超标，但 AI 时序算法预测未来 36 小时内该处渗流将呈现趋势性暴涨，极可能发生**大坝内部管涌与渗透破坏**！系统建议立刻派人前往背水坡现场复核！")
    else:
        st.success("✅ **AI 深度学习引擎状态良好**：当前各测点数据平稳，AI 时序预测未来 48 小时内无大坝结构失稳破坏风险。")

# ------------------------------------------
# Tab 2: CV 视频全时空监控
# ------------------------------------------
with tab2:
    st.header("👁️ 计算机视觉（CV）人员不安全行为与越界监测")
    st.caption("通过智能摄像头自动识别未戴安全帽作业，以及违规侵入防汛红线区域的社会人员。")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📷 01号摄像头：闸门启闭机作业区")
        img = np.zeros((300, 500, 3), dtype=np.uint8) + 100 
        cv2.rectangle(img, (150, 80), (350, 260), (0, 0, 255), 3)
        cv2.putText(img, "WARNING: No Helmet (Unsafe)", (150, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(img, "Worker_01", (150, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # 【全兼容优化】转换格式，并彻底移除静态图片的 key 和容易冲突的适配参数
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        st.image(img_rgb)
        st.warning("⚠️ **违章告警**：检测到运维人员进入闸门检修平台**未佩戴安全帽**！已联动现场蜂鸣器播报驱离。")
        
    with col2:
        st.subheader("📷 02号摄像头：泄洪道下游红线区")
        
        # 【全兼容优化】使用固定的空容器占位符，用来完全根治 React DOM 树的 removeChild 冲突
        video_placeholder = st.empty()
        alert_placeholder = st.empty()
        
        img2 = np.zeros((300, 500, 3), dtype=np.uint8) + 50 
        # 电子围栏基准红线
        cv2.polylines(img2, [np.array([[0,200], [500,200]])], isClosed=False, color=(0,0,255), thickness=3)
        cv2.putText(img2, "DANGER ZONE LINE", (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        # 根据系统控制状态，局部的在占位符内更新视图，杜绝整个结构崩溃
        if st.session_state.cv_alert:
            cv2.rectangle(img2, (200, 120), (280, 250), (0, 0, 255), 2)
            cv2.putText(img2, "INTRUDER: Social Personnel", (170, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
            
            video_placeholder.image(img2_rgb)
            alert_placeholder.error("🚨 **越界告警**：监测到**社会人员翻越围栏**涉水！系统已自动接通附近保安岗亭对讲机。")
        else:
            cv2.putText(img2, "STATUS: CLEAR", (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
            
            video_placeholder.image(img2_rgb)
            alert_placeholder.success("✅ **区域安全**：当前无外部人员非法闯入红线区域。")

# ------------------------------------------
# Tab 3: AI 智能应急指挥中心
# ------------------------------------------
with tab3:
    st.header("🚨 AI 辅助事故应急救援响应程序")
    st.caption("依据《水库大坝安全管理条例》，当大坝发生突发重特大漫坝或溃坝险情时，一键启动 AI 赋能的应急调度。")
    
    # 提供一个一键体验全自动化应急响应的按钮
    if st.button("🔥 模拟突发重特大漫坝/溃坝险情：启动一键应急响应", type="primary", key="btn_emergency_trigger"):
        with st.spinner("⏳ AI 正在根据水利流体力学模型计算灾害演进路线并生成最佳调度方案..."):
            time.sleep(1.5) 
            
        st.error("💥 【应急响应已全面启动】")
        
        ec1, ec2, ec3 = st.columns(3)
        with ec1:
            st.info("🌊 **AI 洪水演进演练**\n\n利用三维大坝BIM模型计算，预计溃坝洪水将在 **18分钟后** 到达下游村庄。已自动向该区域广播及全员手机发送**最高级别疏散指令**。")
        with ec2:
            st.info("🚚 **智能物资与人员调度**\n\nAI 计算最优路线：已自动调度离大坝最近的 3 支抢险队伍和 20 吨防汛沙袋。预计 **12分钟内** 抵达大坝指定防汛位置。")
        with ec3:
            st.info("🛸 **无人机应急出动**\n\n2架智能无人机已自主起飞，正前往泄洪口及下游涉水区执行空中生命迹象搜索，并支持**针对溺水人员智能投掷救生圈**。")
            
        st.success("✅ 应急响应日志已全面同步上传至省防汛抗旱指挥部系统。")
    page_icon="🌊",
    layout="wide"
)

# 使用 Streamlit 的 session_state 来记录和保持用户点击的验证状态
if 'iot_anomaly' not in st.session_state:
    st.session_state.iot_anomaly = False
if 'cv_alert' not in st.session_state:
    st.session_state.cv_alert = False

st.title("🌊 大型水库大坝安全 AI 辅助管理程序原型 (旗舰稳定版)")
st.markdown("---")

# ==========================================
# 2. 侧边栏：系统控制与动态验证沙箱
# ==========================================
st.sidebar.header("⚙️ 系统控制面板")
st.sidebar.subheader("当前监控大坝：高峡水库主坝")

# 模拟 AI 运行状态
ai_status = st.sidebar.selectbox("AI 算法引擎状态", ["正常运行", "算法维护", "离线异常"])
if ai_status == "正常运行":
    st.sidebar.success("🤖 AI 核心引擎已就绪")
else:
    st.sidebar.error("⚠️ AI 引擎未正常工作")

st.sidebar.markdown("---")

# 🧪 互动测试沙箱
st.sidebar.header("🧪 动态验证沙箱 (测试用)")
st.sidebar.markdown("你可以通过以下按钮，手动制造大坝险情，验证 AI 的实时响应能力：")

# 验证控制 1：模拟物联网故障发生
if st.sidebar.button("💥 注入大坝渗流异常数据", type="secondary", key="btn_iot_anomaly"):
    st.session_state.iot_anomaly = True
    st.toast("已成功注入管涌异常数据！请查看 IoT 标签页", icon="📈")

# 验证控制 2：模拟视觉红线越界发生
if st.sidebar.button("🚶 模拟社会人员越界触发红线", type="secondary", key="btn_cv_alert"):
    st.session_state.cv_alert = True
    st.toast("已触发电子红线入侵警报！请查看 CV 标签页", icon="👁️")

# 重置验证按钮
if st.sidebar.button("🔄 恢复系统至安全状态", type="primary", key="btn_reset_all"):
    st.session_state.iot_anomaly = False
    st.session_state.cv_alert = False
    st.toast("系统已重置，全部指标恢复正常安全水平。", icon="✅")

st.sidebar.markdown("---")
st.sidebar.info("""
**设计说明**：本程序严格遵循课程设计任务书要求，融合了物联网（IoT）时序预测与计算机视觉（CV）技术，实现大坝防汛与作业安全的智能化管控。
""")

# ==========================================
# 3. 核心功能划分（Tabs 标签页）
# ==========================================
tab1, tab2, tab3 = st.tabs(["📊 IoT 大坝结构渗流监测 (时序预测)", "👁️ CV 视频全时空监控 (行为识别)", "🚨 AI 智能应急指挥中心"])

# ------------------------------------------
# Tab 1: IoT 大坝结构渗流监测
# ------------------------------------------
with tab1:
    st.header("📈 基于 LSTM 算法的渗流与位移失稳预警")
    st.caption("利用物联网传感器收集渗压、水位数据，AI 预测未来48小时走势，实现隐患早发现。")
    
    # 动态数据发生器：根据侧边栏是否注入异常，改变生成的数学模型
    np.random.seed(42)
    time_axis = np.arange(-24, 48)
    
    if st.session_state.iot_anomaly:
        # 🚨 异常状态：AI 预测曲线呈现急剧指数级上升（模拟管涌）
        actual_data = np.concatenate([np.random.normal(5, 0.2, 25), [np.nan]*47])
        predict_data = np.concatenate([[np.nan]*24, [5.0], np.cumsum(np.random.uniform(0.1, 0.6, 47)) + 5])
    else:
        # ✅ 安全状态：AI 预测曲线在正常范围内平稳波动
        actual_data = np.concatenate([np.random.normal(5, 0.2, 25), [np.nan]*47])
        predict_data = np.concatenate([[np.nan]*24, [5.0], np.random.normal(5, 0.25, 47)])
        
    chart_data = pd.DataFrame({
        '时间 (小时后)': time_axis,
        '实际观测值 (mm)': actual_data,
        'AI 预测走势 (mm)': predict_data
    })
    
    # 使用 Plotly 绘制动态预测曲线
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=chart_data['时间 (小时后)'], y=chart_data['实际观测值 (mm)'], name='过去24小时实际渗流量', mode='lines+markers', line=dict(color='blue')))
    
    if st.session_state.iot_anomaly:
        fig.add_trace(go.Scatter(x=chart_data['时间 (小时后)'], y=chart_data['AI 预测走势 (mm)'], name='AI 预警：渗流指数级恶化 (存在管涌风险)', mode='lines', line=dict(color='red', dash='dash')))
    else:
        fig.add_trace(go.Scatter(x=chart_data['时间 (小时后)'], y=chart_data['AI 预测走势 (mm)'], name='AI 预测：未来48小时运行平稳', mode='lines', line=dict(color='green', dash='dash')))
        
    fig.update_layout(title="大坝背水坡 AP-03 测点渗流量实时预测图", xaxis_title="时间轴 (当前为 0 时刻)", yaxis_title="渗流量 (mm/d)")
    st.plotly_chart(fig, use_container_width=True, key="plotly_iot_chart")
    
    # 动态简报框展现
    if st.session_state.iot_anomaly:
        st.warning("⚠️ **AI 深度学习引擎预警简报**：监测到 AP-03 测点虽然当前数据（5.0mm）尚未超标，但 AI 时序算法预测未来 36 小时内该处渗流将呈现趋势性暴涨，极可能发生**大坝内部管涌与渗透破坏**！系统建议立刻派人前往背水坡现场复核！")
    else:
        st.success("✅ **AI 深度学习引擎状态良好**：当前各测点数据平稳，AI 时序预测未来 48 小时内无大坝结构失稳破坏风险。")

# ------------------------------------------
# Tab 2: CV 视频全时空监控
# ------------------------------------------
with tab2:
    st.header("👁️ 计算机视觉（CV）人员不安全行为与越界监测")
    st.caption("通过智能摄像头自动识别未戴安全帽作业，以及违规侵入防汛红线区域的社会人员。")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📷 01号摄像头：闸门启闭机作业区")
        img = np.zeros((300, 500, 3), dtype=np.uint8) + 100 
        cv2.rectangle(img, (150, 80), (350, 260), (0, 0, 255), 3)
        cv2.putText(img, "WARNING: No Helmet (Unsafe)", (150, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(img, "Worker_01", (150, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        # 【修正优化】转换格式并移除引起兼容问题的参数
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        st.image(img_rgb, key="img_camera_01")
        st.warning("⚠️ **违章告警**：检测到运维人员进入闸门检修平台**未佩戴安全帽**！已联动现场蜂鸣器播报驱离。")
        
    with col2:
        st.subheader("📷 02号摄像头：泄洪道下游红线区")
        img2 = np.zeros((300, 500, 3), dtype=np.uint8) + 50 
        
        # 电子围栏基准红线
        cv2.polylines(img2, [np.array([[0,200], [500,200]])], isClosed=False, color=(0,0,255), thickness=3)
        cv2.putText(img2, "DANGER ZONE LINE", (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        
        # 根据侧边栏控制，动态渲染是否有入侵者
        if st.session_state.cv_alert:
            cv2.rectangle(img2, (200, 120), (280, 250), (0, 0, 255), 2)
            cv2.putText(img2, "INTRUDER: Social Personnel", (170, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
            st.image(img2_rgb, key="img_camera_02_alert")
            st.error("🚨 **越界告警**：监测到**社会人员翻越围栏**涉水！系统已自动接通附近保安岗亭对讲机。")
        else:
            cv2.putText(img2, "STATUS: CLEAR", (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
            st.image(img2_rgb, key="img_camera_02_clear")
            st.success("✅ **区域安全**：当前无外部人员非法闯入红线区域。")

# ------------------------------------------
# Tab 3: AI 智能应急指挥中心
# ------------------------------------------
with tab3:
    st.header("🚨 AI 辅助事故应急救援响应程序")
    st.caption("依据《水库大坝安全管理条例》，当大坝发生突发重特大漫坝或溃坝险情时，一键启动 AI 赋能的应急调度。")
    
    # 提供一个一键体验全自动化应急响应的按钮
    if st.button("🔥 模拟突发重特大漫坝/溃坝险情：启动一键应急响应", type="primary", key="btn_emergency_trigger"):
        with st.spinner("⏳ AI 正在根据水利流体力学模型计算灾害演进路线并生成最佳调度方案..."):
            time.sleep(1.5) 
            
        st.error("💥 【应急响应已全面启动】")
        
        ec1, ec2, ec3 = st.columns(3)
        with ec1:
            st.info("🌊 **AI 洪水演进演练**\n\n利用三维大坝BIM模型计算，预计溃坝洪水将在 **18分钟后** 到达下游村庄。已自动向该区域广播及全员手机发送**最高级别疏散指令**。")
        with ec2:
            st.info("🚚 **智能物资与人员调度**\n\nAI 计算最优路线：已自动调度离大坝最近的 3 支抢险队伍和 20 吨防汛沙袋。预计 **12分钟内** 抵达大坝指定防汛位置。")
        with ec3:
            st.info("🛸 **无人机应急出动**\n\n2架智能无人机已自主起飞，正前往泄洪口及下游涉水区执行空中生命迹象搜索，并支持**针对溺水人员智能投掷救生圈**。")
            
        st.success("✅ 应急响应日志已全面同步上传至省防汛抗旱指挥部系统。")
