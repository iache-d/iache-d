public class Main {
    public static void main(String[] args) {
        int a = 5;
        int b = 7;
        int r = 3;
        int h = 6;

        FiguraGeometrica[] figuras = new FiguraGeometrica[8];

        figuras[0] = new Cuadrado(a);
        figuras[1] = new Rectangulo(a, b);
        figuras[2] = new Triangulo(a, b, a);
        figuras[3] = new Circulo(r);
        figuras[4] = new Esfera(r);
        figuras[5] = new Cubo(a);
        figuras[6] = new Tetraedro(a);
        figuras[7] = new Cilindro(r, h);

        for (int i = 0; i < figuras.length; i++) {
            figuras[i].ResumenFigura();
        }
    }
}
