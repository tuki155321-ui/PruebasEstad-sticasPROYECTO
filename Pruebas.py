"""
Asistente para Selección de Pruebas Estadísticas
GitHub: https://github.com/tu_usuario/selector_pruebas_estadisticas
"""

def asistente_pruebas_estadisticas():
    """
    Asistente interactivo que guía en la selección de la prueba estadística apropiada
    basado en el tipo de datos y objetivo de investigación.
    """
    
    print("🎯 ASISTENTE PARA SELECCIÓN DE PRUEBAS ESTADÍSTICAS")
    print("=" * 50)
    print("Responde las siguientes preguntas sobre tus datos:\n")
    
    # Pregunta 1: Tipo de variables
    print("1. ¿Qué tipo de variables quieres analizar?")
    print("   a) Comparar grupos (ej: Grupo A vs Grupo B)")
    print("   b) Relación entre variables (ej: Edad vs Peso)")
    print("   c) Asociación entre categorías (ej: Género vs Preferencia)")
    
    opcion1 = input("   Selecciona (a/b/c): ").lower()
    
    if opcion1 == "a":
        # Análisis de grupos
        print("\n2. ¿Cuántos grupos quieres comparar?")
        print("   a) 2 grupos")
        print("   b) 3 o más grupos")
        
        opcion2 = input("   Selecciona (a/b): ").lower()
        
        if opcion2 == "a":
            print("\n3. ¿Los grupos son independientes o relacionados/emparejados?")
            print("   a) Independientes (ej: Hombres vs Mujeres)")
            print("   b) Relacionados/Emparejados (ej: Antes vs Después)")
            
            opcion3 = input("   Selecciona (a/b): ").lower()
            
            if opcion3 == "a":
                print("\n4. ¿Tus datos cumplen supuestos de normalidad?")
                print("   a) Sí, son normales y hay homocedasticidad")
                print("   b) No, no cumplen supuestos paramétricos")
                
                opcion4 = input("   Selecciona (a/b): ").lower()
                
                if opcion4 == "a":
                    recomendacion = "t de Student para muestras independientes"
                    razon = "Comparas 2 grupos independientes con datos normales"
                else:
                    recomendacion = "U de Mann-Whitney"
                    razon = "Comparas 2 grupos independientes sin normalidad"
                    
            else:  # Grupos relacionados
                print("\n4. ¿Las diferencias entre pares son normales?")
                print("   a) Sí, las diferencias son normales")
                print("   b) No, no hay normalidad en las diferencias")
                
                opcion4 = input("   Selecciona (a/b): ").lower()
                
                if opcion4 == "a":
                    recomendacion = "t de Student para muestras relacionadas"
                    razon = "Comparas mediciones repetidas con diferencias normales"
                else:
                    recomendacion = "Wilcoxon"
                    razon = "Comparas mediciones repetidas sin normalidad"
                    
        else:  # 3 o más grupos
            print("\n3. ¿Los datos cumplen supuestos de normalidad?")
            print("   a) Sí, son normales y hay homocedasticidad")
            print("   b) No, no cumplen supuestos paramétricos")
            
            opcion3 = input("   Selecciona (a/b): ").lower()
            
            if opcion3 == "a":
                recomendacion = "ANOVA de un factor"
                razon = "Comparas 3 o más grupos independientes con datos normales"
            else:
                recomendacion = "Kruskal-Wallis"
                razon = "Comparas 3 o más grupos independientes sin normalidad"
                
    elif opcion1 == "b":
        # Relación entre variables
        print("\n2. ¿Qué tipo de relación quieres analizar?")
        print("   a) Relación lineal entre variables cuantitativas")
        print("   b) Relación monótona (no necesariamente lineal)")
        print("   c) Predecir una variable a partir de otra")
        
        opcion2 = input("   Selecciona (a/b/c): ").lower()
        
        if opcion2 == "a":
            print("\n3. ¿Los datos cumplen supuestos de normalidad?")
            print("   a) Sí, ambas variables son normales")
            print("   b) No, no hay normalidad bivariada")
            
            opcion3 = input("   Selecciona (a/b): ").lower()
            
            if opcion3 == "a":
                recomendacion = "Correlación de Pearson"
                razon = "Mides relación lineal entre variables normales"
            else:
                recomendacion = "Correlación de Spearman"
                razon = "Mides relación monótona sin requerir normalidad"
                
        elif opcion2 == "b":
            recomendacion = "Correlación de Spearman"
            razon = "Mides relación monótona (no necesariamente lineal)"
            
        else:  # Predicción
            print("\n3. ¿Quieres predecir una variable a partir de otra?")
            print("   a) Sí, modelo de regresión lineal")
            print("   b) Solo ver la relación")
            
            opcion3 = input("   Selecciona (a): ").lower()
            
            recomendacion = "Regresión lineal simple"
            razon = "Modelas y predices una variable en función de otra"
            
    else:  # Asociación entre categorías
        print("\n2. ¿Analizas frecuencias en categorías?")
        print("   a) Sí, tabla de contingencia")
        print("   b) No, son variables diferentes")
        
        opcion2 = input("   Selecciona (a): ").lower()
        
        recomendacion = "Chi-cuadrada"
        razon = "Analizas asociación entre variables categóricas"
    
    # Mostrar recomendación final
    print("\n" + "=" * 50)
    print("📊 RECOMENDACIÓN FINAL")
    print("=" * 50)
    print(f"Prueba recomendada: {recomendacion}")
    print(f"Razón: {razon}")
    
    # Información adicional
    print("\n💡 INFORMACIÓN ADICIONAL:")
    if "paramétrica" in recomendacion.lower() or recomendacion in ["t de Student", "ANOVA", "Pearson", "Regresión lineal"]:
        print("   - Es una prueba PARAMÉTRICA")
        print("   - Requiere verificación de supuestos")
    else:
        print("   - Es una prueba NO PARAMÉTRICA")
        print("   - Más robusta, menos supuestos")
    
    print("\n⚠️  RECUERDA:")
    print("   - Siempre verifica los supuestos antes de aplicar")
    print("   - Considera el tamaño de muestra")
    print("   - Revisa outliers y calidad de datos")

def mostrar_arbol_decision():
    """
    Muestra un resumen del árbol de decisión
    """
    print("\n🌳 RESUMEN DEL ÁRBOL DE DECISIÓN:")
    print("""
    1. ¿Comparar grupos?
       ├── 2 grupos?
       │   ├── Independientes?
       │   │   ├── Normales? → t-Student independientes
       │   │   └── No normales? → Mann-Whitney
       │   └── Relacionados?
       │       ├── Diferencias normales? → t-Student relacionados
       │       └── No normales? → Wilcoxon
       └── 3+ grupos?
           ├── Normales? → ANOVA
           └── No normales? → Kruskal-Wallis
    
    2. ¿Relación entre variables?
       ├── Lineal + Normales? → Pearson
       ├── Monótona/No lineales? → Spearman
       └── Predicción? → Regresión lineal
    
    3. ¿Asociación categórica? → Chi-cuadrada
    """)

# Ejecutar el asistente
if __name__ == "__main__":
    try:
        asistente_pruebas_estadisticas()
        
        # Preguntar si quiere ver el árbol de decisión
        ver_arbol = input("\n¿Quieres ver el árbol de decisión completo? (s/n): ").lower()
        if ver_arbol == 's':
            mostrar_arbol_decision()
            
        print("\n✅ ¡Listo! Puedes usar este código en GitHub para tus proyectos.")
        
    except KeyboardInterrupt:
        print("\n❌ Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n⚠️  Error: {e}")
