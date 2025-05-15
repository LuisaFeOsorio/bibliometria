package model;

import java.util.Objects;

public class Producto {
    private String titulo;
    private String autores;
    private String resumen;
    private int anio;
    private String tipo;  // Artículo, conferencia, libro, etc.

    // Constructor
    public Producto(String titulo, String autores, String resumen, int anio, String tipo) {
        this.titulo = titulo;
        this.autores = autores;
        this.resumen = resumen;
        this.anio = anio;
        this.tipo = tipo;
    }

    // Getters y Setters
    public String getTitulo() {
        return titulo;
    }

    public String getAutores() {
        return autores;
    }

    public String getResumen() {
        return resumen;
    }

    public int getAnio() {
        return anio;
    }

    public String getTipo() {
        return tipo;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Producto producto = (Producto) o;
        return titulo.equals(producto.titulo) && autores.equals(producto.autores);
    }

    @Override
    public int hashCode() {
        return Objects.hash(titulo, autores);
    }
}
