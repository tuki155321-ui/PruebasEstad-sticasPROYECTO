import streamlit as st
import pandas as pd
import json
from pathlib import Path

# Configuración de la página
st.set_page_config(
    page_title="Selector de Pruebas Estadísticas",
    page_icon="📊",
    layout="centered"
)

# Datos del flujo de decisión
DECISION_FLOW = {
    "start": {
        "question": "🎯 ¿QUÉ TIPO DE ANÁLISIS NECESITAS?",
        "options": {
            "A": "COMPARAR grupos o condiciones",
            "B": "ANALIZAR relación entre variables", 
            "C": "VER asociación entre categorías",
            "D": "PREDECIR una variable"
        },
        "next": {
            "A": "comparison",
            "B": "relationship", 
            "C": "chi_square",
            "D": "regression"
        }
    },
    
    "comparison": {
        "question": "🔢 ¿CUÁNTOS GRUPOS COMPARAS?",
        "options": {
            "A": "2 grupos",
            "B": "3 o más grupos"
        },
        "next": {
            "A": "two_groups",
            "B": "multiple_groups"
        }
    },
    
    "two_groups": {
        "question": "🔄 ¿QUÉ TIPO DE GRUPOS TIENES?",
        "options": {
            "A": "INDEPENDIENTES (ej: hombres vs mujeres)",
            "B": "RELACIONADOS/EMPAREJADOS (ej: antes vs después)"
        },
        "next": {
            "A": "independent_groups",
            "B": "related_groups"
        }
    },
    
    "independent_groups": {
        "question": "📈 ¿TUS DATOS CUMPLEN NORMALIDAD?",
        "options": {
            "A": "SÍ, datos normales y homocedasticidad",
            "B": "NO, no cumplen supuestos paramétricos"
        },
        "result": {
            "A": "🧪 t de Student para muestras INDEPENDIENTES",
            "B": "📊 U de Mann-Whitney"
        }
    },
    
    "related_groups": {
        "question": "📈 ¿LAS DIFERENCIAS ENTRE PARES SON NORMALES?",
        "options": {
            "A": "SÍ, diferencias normales",
            "B": "NO, no hay normalidad en diferencias"
        },
        "result": {
            "A": "🧪 t de Student para muestras RELACIONADAS", 
            "B": "📊 Prueba de Wilcoxon"
        }
    },
    
    "multiple_groups": {
        "question": "📈 ¿TUS DATOS CUMPLEN NORMALIDAD?",
        "options": {
            "A": "SÍ, datos normales y homocedasticidad",
            "B": "NO, no cumplen supuestos paramétricos"
        },
        "result": {
            "A": "🧪 ANOVA de un factor",
            "B": "📊 Prueba de Kruskal-Wallis"
        }
    },
    
    "relationship": {
        "question": "📈 ¿QUÉ TIPO DE RELACIÓN ESTUDIAS?",
        "options": {
            "A": "RELACIÓN LINEAL entre variables cuantitativas",
            "B": "RELACIÓN MONÓTONA (no necesariamente lineal)"
        },
        "next": {
            "A": "linear_relationship",
            "B": "spearman_result"
        }
    },
    
    "linear_relationship": {
        "question": "📊 ¿TUS VARIABLES SON NORMALES?",
        "options": {
            "A": "SÍ, ambas variables normales",
            "B": "NO, alguna variable no es normal"
        },
        "result": {
            "A": "🧪 Correlación de Pearson",
            "B": "📊 Correlación de Spearman"
        }
    },
    
    "spearman_result": {
        "question": "ℹ️ INFORMACIÓN ADICIONAL",
        "info": "La correlación de Spearman es ideal para relaciones monótonas",
        "result": "📊 Correlación de Spearman"
    },
    
    "chi_square": {
        "question": "✅ CONFIRMACIÓN",
        "info": "Analizarás asociación entre variables categóricas",
        "result": "📊 Prueba Chi-cuadrada"
    },
    
    "regression": {
        "question": "✅ CONFIRMACIÓN", 
        "info": "Modelarás y predecirás una variable en función de otra",
        "result": "🧪 Regresión lineal simple"
    }
}

# Información detallada de cada prueba
TEST_INFO = {
    "🧪 t de Student para muestras INDEPENDIENTES": {
        "tipo": "Paramétrica",
        "supuestos": [
            "Datos en escala intervalar o racional",
            "Distribución normal en cada grupo", 
            "Homocedasticidad (varianzas similares)",
            "Observaciones independientes"
        ],
        "usos": "Comparar medias de 2 grupos independientes"
    },
    
    "🧪 t de Student para muestras RELACIONADAS": {
        "tipo": "Paramétrica", 
        "supuestos": [
            "Datos en escala intervalar o racional",
            "Diferencias entre pares distribuidas normalmente",
            "Observaciones emparejadas o dependientes"
        ],
        "usos": "Comparar medias de mediciones repetidas"
    },
    
    "📊 U de Mann-Whitney": {
        "tipo": "No paramétrica",
        "supuestos": [
            "Escala ordinal, intervalar o racional",
            "No requiere normalidad",
            "Evalúa diferencias en medianas o posiciones"
        ],
        "usos": "Comparar 2 grupos independientes sin normalidad"
    },
    
    "📊 Prueba de Wilcoxon": {
        "tipo": "No paramétrica",
        "supuestos": [
            "Escala ordinal, intervalar o racional", 
            "No requiere normalidad en diferencias",
            "Observaciones emparejadas"
        ],
        "usos": "Comparar 2 grupos relacionados sin normalidad"
    },
    
    "🧪 ANOVA de un factor": {
        "tipo": "Paramétrica",
        "supuestos": [
            "Datos en escala intervalar o racional",
            "Distribución normal en cada grupo",
            "Homocedasticidad entre grupos",
            "Observaciones independientes"
        ],
        "usos": "Comparar medias de 3 o más grupos independientes"
    },
    
    "📊 Prueba de Kruskal-Wallis": {
        "tipo": "No paramétrica", 
        "supuestos": [
            "Escala ordinal, intervalar o racional",
            "No requiere normalidad",
            "Evalúa diferencias en medianas de múltiples grupos"
        ],
        "usos": "Comparar 3 o más grupos sin normalidad"
    },
    
    "🧪 Correlación de Pearson": {
        "tipo": "Paramétrica",
        "supuestos": [
            "Ambas variables cuantitativas",
            "Relación lineal entre variables", 
            "Distribución normal bivariada",
            "Homocedasticidad"
        ],
        "usos": "Medir fuerza y dirección de relación lineal"
    },
    
    "📊 Correlación de Spearman": {
        "tipo": "No paramétrica",
        "supuestos": [
            "Escala ordinal, intervalar o racional",
            "No requiere normalidad",
            "Evalúa relaciones monótonas"
        ],
        "usos": "Medir fuerza y dirección de relación monótona"
    },
    
    "📊 Prueba Chi-cuadrada": {
        "tipo": "No paramétrica", 
        "supuestos": [
            "Variables categóricas",
            "Frecuencias esperadas ≥ 5",
            "Observaciones independientes"
        ],
        "usos": "Analizar asociación entre variables categóricas"
    },
    
    "🧪 Regresión lineal simple": {
        "tipo": "Paramétrica",
        "supuestos": [
            "Variable dependiente cuantitativa", 
            "Relación lineal entre variables",
            "Residuos distribuidos normalmente",
            "Homocedasticidad de residuos",
            "Independencia de observaciones"
        ],
        "usos": "Predecir variable dependiente en función de independiente"
    }
}

def main():
    # Header
    st.title("📊 Selector de Pruebas Estadísticas")
    st.markdown("---")
    
    # Inicializar estado de sesión
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'start'
        st.session_state.path = []
        st.session_state.final_result = None
    
    # Mostrar progreso
    if st.session_state.path:
        st.subheader("🗺️ Tu ruta:")
        path_display = " → ".join(st.session_state.path)
        st.info(path_display)
    
    # Obtener paso actual - CORRECCIÓN AQUÍ: st.session_state no str.session_state
    current_step = DECISION_FLOW[st.session_state.current_step]
    
    # Mostrar pregunta
    st.subheader(current_step["question"])
    
    # Mostrar información adicional si existe
    if "info" in current_step:
        st.info(current_step["info"])
    
    # Mostrar opciones
    selected_option = None
    col1, col2 = st.columns(2)
    
    options = list(current_step["options"].items())
    for i, (key, value) in enumerate(options):
        with col1 if i % 2 == 0 else col2:
            if st.button(f"**{key}**: {value}", use_container_width=True):
                selected_option = key
    
    # Procesar selección
    if selected_option:
        # Guardar en el historial
        st.session_state.path.append(current_step["options"][selected_option])
        
        # Verificar si es resultado final
        if "result" in current_step:
            st.session_state.final_result = current_step["result"][selected_option]
            st.session_state.current_step = "result"
        else:
            # Avanzar al siguiente paso
            st.session_state.current_step = current_step["next"][selected_option]
        
        # Recargar la página
        st.rerun()
    
    # Mostrar resultado final
    if st.session_state.current_step == "result" and st.session_state.final_result:
        st.markdown("---")
        st.success("🎉 **PRUEBA RECOMENDADA**")
        
        result_key = st.session_state.final_result
        st.header(f"**{result_key}**")
        
        # Mostrar información detallada
        info = TEST_INFO[result_key]
        
        st.subheader("📋 Información de la prueba:")
        st.write(f"**Tipo:** {info['tipo']}")
        st.write(f"**Uso principal:** {info['usos']}")
        
        st.subheader("✅ Supuestos que deben cumplirse:")
        for supuesto in info['supuestos']:
            st.write(f"• {supuesto}")
        
        # Botón para reiniciar
        st.markdown("---")
        if st.button("🔄 Realizar nueva consulta", use_container_width=True):
            st.session_state.current_step = 'start'
            st.session_state.path = []
            st.session_state.final_result = None
            st.rerun()

    # Footer
    st.markdown("---")
    st.caption("Desarrollado con Streamlit • Basado en criterios estadísticos estándar")

if __name__ == "__main__":
    main()
