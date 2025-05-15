package leerDatos;

import model.Producto;

import java.io.*;
import java.util.*;

public class LectorBibTex {

    public List<Producto> leerBibTex(String archivo) throws IOException {
        List<Producto> productos = new ArrayList<>();
        BufferedReader br = new BufferedReader(new FileReader(archivo));
        String linea;

        String titulo = null;
        String autores = null;
        String resumen = null;
        int anio = 0;
        String tipo = null;

        while ((linea = br.readLine()) != null) {
            if (linea.startsWith("title = {")) {
                titulo = linea.substring(8, linea.length() - 1).trim();
            } else if (linea.startsWith("author = {")) {
                autores = linea.substring(10, linea.length() - 1).trim();
            } else if (linea.startsWith("abstract = {")) {
                resumen = linea.substring(12, linea.length() - 1).trim();
            } else if (linea.startsWith("year = {")) {
                anio = Integer.parseInt(linea.substring(8, linea.length() - 1).trim());
            } else if (linea.startsWith("type = {")) {
                tipo = linea.substring(8, linea.length() - 1).trim();
            }

            if (linea.startsWith("}")) { // Fin de un artículo
                if (titulo != null && autores != null && resumen != null && anio > 0 && tipo != null) {
                    Producto producto = new Producto(titulo, autores, resumen, anio, tipo);
                    productos.add(producto);
                }
                // Reset para el siguiente artículo
                titulo = null;
                autores = null;
                resumen = null;
                anio = 0;
                tipo = null;
            }
        }

        br.close();
        return productos;
    }
}

