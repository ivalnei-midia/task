import streamlit as st
import database as db
from datetime import datetime
import time
import os
import getpass
# Configuração da página
st.set_page_config(
    page_title="TaskFlow | Gerenciador Moderno de Tarefas",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed"  # Sidebar começa recolhida em dispositivos móveis
)

# Função para carregar CSS externo
def load_external_css():
    css_file = os.path.join(os.path.dirname(__file__), "static", "style.css")
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_external_css()


# Inicialização do banco de dados
db.init_db()

# Funções do banco de dados (mantidas como antes)
def get_tasks(filter_status=None, filter_priority=None, filter_usuario=None):
    conn = db.get_connection()
    cursor = conn.cursor()
    
    if filter_status is not None and filter_priority is not None and filter_usuario is not None:
        cursor.execute("""
            SELECT id, description, completed, created_at, priority, usuario 
            FROM tasks 
            WHERE completed = %s AND priority = %s AND usuario = %s
            ORDER BY created_at DESC
        """, (filter_status, filter_priority, filter_usuario))
    elif filter_status is not None and filter_priority is not None:
        cursor.execute("""
            SELECT id, description, completed, created_at, priority, usuario 
            FROM tasks 
            WHERE completed = %s AND priority = %s 
            ORDER BY created_at DESC
        """, (filter_status, filter_priority))
    elif filter_status is not None and filter_usuario is not None:
        cursor.execute("""
            SELECT id, description, completed, created_at, priority, usuario 
            FROM tasks 
            WHERE completed = %s AND usuario = %s
            ORDER BY created_at DESC
        """, (filter_status, filter_usuario))
    elif filter_priority is not None and filter_usuario is not None:
        cursor.execute("""
            SELECT id, description, completed, created_at, priority, usuario 
            FROM tasks 
            WHERE priority = %s AND usuario = %s
            ORDER BY created_at DESC
        """, (filter_priority, filter_usuario))
    elif filter_status is not None:
        cursor.execute("""
            SELECT id, description, completed, created_at, priority, usuario 
            FROM tasks 
            WHERE completed = %s 
            ORDER BY created_at DESC
        """, (filter_status,))
    elif filter_priority is not None:
        cursor.execute("""
            SELECT id, description, completed, created_at, priority, usuario 
            FROM tasks 
            WHERE priority = %s 
            ORDER BY created_at DESC
        """, (filter_priority,))
    elif filter_usuario is not None:
        cursor.execute("""
            SELECT id, description, completed, created_at, priority, usuario 
            FROM tasks 
            WHERE usuario = %s
            ORDER BY created_at DESC
        """, (filter_usuario,))
    else:
        cursor.execute("""
            SELECT id, description, completed, created_at, priority, usuario 
            FROM tasks 
            ORDER BY created_at DESC
        """)
    
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks

def add_task(description, priority, usuario):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (description, priority, usuario) VALUES (%s, %s, %s) RETURNING id", (description, priority, usuario))
    task_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return task_id

def update_task(task_id, completed):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = %s WHERE id = %s", (completed, task_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_task(task_id):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()


# Obter o usuário logado do Windows
usuario = getpass.getuser()
data_atual = datetime.now().strftime("%d/%m/%Y")
# Layout principal
#st.title(st.markdown("<sidebar-text>📋 Fluxo de tarefas</sidebar-text>", unsafe_allow_html=True))
with st.container():
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown("<h1 style='color: rgba(153,192,34,1);'>📋 Fluxo de tarefas</h1>", unsafe_allow_html=True)
    with col2:
        st.write(f"Bem vindo <div style='color: rgba(153,192,34,1);font-weight: bold;'>{usuario.upper()}</div>{data_atual}", unsafe_allow_html=True)

# Adicionar logo usando HTML/CSS


# Formulário para adicionar nova tarefa
with st.form("new_task_form"):
    cols = st.columns([5, 1, 1])  # Ajustado para incluir o select de prioridade
    with cols[0]:
        new_task = st.text_input("Nova tarefa", placeholder="O que precisa ser feito?", label_visibility="collapsed")
    with cols[1]:
        priority = st.selectbox(
            "Prioridade",
            options=[0, 1, 2],
            format_func=lambda x: ["Baixa", "Média", "Alta"][x],
            label_visibility="collapsed"
        )
    with cols[2]:
        submitted = st.form_submit_button("Adicionar", use_container_width=True)
    
    if submitted and new_task:
        task_id = add_task(new_task, priority,usuario)
        st.success("Tarefa adicionada com sucesso!")
        time.sleep(0.5)
        st.rerun()
        

# logo  da Ebserh
with st.sidebar:
    st.image("img/ebserh.jpg")
    st.markdown("""
    <style>
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;    
    </style>
    """, unsafe_allow_html=True)

# Definir filtros e buscar tarefas
filter_status = st.sidebar.radio(
    "Status das Tarefas",
    ["Todas", "Pendentes", "Concluídas"],
    index=0,
    horizontal=True
)

priority_filter = st.sidebar.radio(
    "Filtrar por prioridade",
    options=["Todas", "Baixa", "Média", "Alta"],
    index=0,
    horizontal=True
)

# Opção para filtrar por usuário logado
minhas_tarefas = st.sidebar.checkbox("Mostrar apenas minhas tarefas", value=False)

# Converter filtros para valores apropriados
status_value = None if filter_status == "Todas" else (True if filter_status == "Concluídas" else False)
priority_value = None if priority_filter == "Todas" else ["Baixa", "Média", "Alta"].index(priority_filter)

# Aplicar filtro por usuário somente se o checkbox estiver marcado
usuario_filtro = usuario if minhas_tarefas else None

# Buscar tarefas com os filtros
tasks = get_tasks(filter_status=status_value, filter_priority=priority_value, filter_usuario=usuario_filtro)

# Adicionar informação sobre o filtro de usuário
if tasks:
    filtro_info = f"Status: <span style='color: rgba(153,192,34,1); font-weight: bold;'>{filter_status}</span> - Prioridade: <span style='color: rgba(153,192,34,1); font-weight: bold;'>{priority_filter}</span>"
    if minhas_tarefas:
        filtro_info += f" - Usuário: <span style='color: rgba(153,192,34,1); font-weight: bold;'>{usuario.upper()}</span>"
    st.write(filtro_info, unsafe_allow_html=True)

# Sidebar com estatísticas
with st.sidebar:
    
    st.markdown("## 📊 Estatísticas")
    if tasks:
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task[2])
        progress = (completed_tasks / total_tasks) if total_tasks > 0 else 0
        st.metric("Tarefas Concluídas", f"{completed_tasks}/{total_tasks}")
        st.progress(progress, text=f"{progress * 100:.0f}%")
    else:
        st.metric("Tarefas Concluídas", "0/0")
        st.progress(0, text="0%")

# Lista de tarefas
if tasks:
    st.subheader("Lista de Tarefas") 
    #st.write(f"Status: <span style='color: rgba(153,192,34,1); font-weight: bold;'>{filter_status}</span> - Prioridade: <span style='color: rgba(153,192,34,1); font-weight: bold;'>{priority_filter}</span>", unsafe_allow_html=True)
    #st.divider()

    for task in tasks:
        task_id, description, completed, created_at, priority, usuario_task = task  # Adicionado usuario_task
        created_str = created_at.strftime("%d/%m/%Y %H:%M")
        if completed:
            # Data atual para o momento da conclusão
            completion_date = datetime.now()
            finally_str = " - Finalizada em: " + completion_date.strftime("%d/%m/%Y %H:%M")
            # Calcular diferença em dias
            time_delta = completion_date - created_at
            days_delta = time_delta.days
            if days_delta == 0:
                time_message = " (concluída no mesmo dia)"
            elif days_delta == 1:
                time_message = " (concluída em 1 dia)"
            else:
                time_message = f" (concluída em {days_delta} dias)"
            finally_str += time_message
        else:
            finally_str = ""
            days_delta = ""
        with st.container():
            col1, col2, col3, col4 = st.columns([5, 0.2, 0.3, 0.3])
            with col1:
                st.markdown(f"""
                <div class="task-card {'completed' if completed else ''}" style="padding: 0.5rem;">
                    <div class="task-content" style="display: flex; flex-direction: column; gap: 0.5rem;">
                        <div class="task-text {'completed' if completed else ''}" style="font-size: 1rem;">
                            <div style="font-weight: bold;">{description}</div> Criada em: {created_str} por {usuario_task.upper()} {finally_str}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown(f"""
                    <div class="task-content" style="display: flex; align-items: center; justify-content: center;">
                        <!--{st.checkbox("", value=completed, key=f"check_{task_id}", on_change=update_task, args=(task_id, not completed))}-->
                    </div>
                """, unsafe_allow_html=True)
                
            with col3:
                
                st.markdown(f"""
                <div class="task-actions" style="display: flex; align-items: center; justify-content: center;">
                    <!--{st.button("🗑️", key=f"del_{task_id}", on_click=delete_task, args=(task_id,), help="Excluir tarefa")}-->
                </div>
                """, unsafe_allow_html=True)
            
            with col4:                
                priority_labels = ["🔵 Baixa", "🟢 Média", "🔴 Alta "]
                st.markdown(f"""
                <div class="task-actions" style="display: flex; align-items: left; justify-content: left; color: {priority_labels[priority]};">
                    <b>{priority_labels[priority]}</b>
                </div>
                """, unsafe_allow_html=True)
                        


           
else:
    st.info("🎉 Você não tem tarefas! Adicione uma nova acima.")




