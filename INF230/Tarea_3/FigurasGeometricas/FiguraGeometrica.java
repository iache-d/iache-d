public abstract class FiguraGeometrica {
    protected String nombre;
    protected String tipo;

    public FiguraGeometrica(String nombre) {
        this.nombre = nombre;
    }

    // ⚠ CAMBIAMOS visibilidad de GetNombre() a public
    // para poder acceder a ella desde otras clases
    // Cambié la visibilidad a public porque necesito acceder al nombre desde otras clases concretas para imprimir en ResumenFigura()
    // Sí, dejaré este comentario un poco como broma, sucede que cuando hice esta parte del código puse los dos primeros comentarios, pero lo dejé privado sin querer, por ende algo fallaba, al darme cuenta volví y lo cambié y coloqué el tercer comentario, luego leí los dos primeros...
    public final String GetNombre() {
    return this.nombre;
    }


    protected final String GetTipo() {
        return this.tipo;
    }

    abstract protected void ResumenFigura();
}
