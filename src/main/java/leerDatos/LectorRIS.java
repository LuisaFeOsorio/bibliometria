package leerDatos;

import model.Producto;

import java.io.*;
import java.util.*;

public class LectorRIS {

    public List<Producto> leerRIS(String archivo) throws IOException {
        List<Producto> productos = new ArrayList<>();
        BufferedReader br = new BufferedReader(new FileReader(archivo));
        String linea;

        String titulo = null;
        String autores = null;
        String resumen = null;
        int anio = 0;
        String tipo = null;

        while ((linea = br.readLine()) != null) {
            if (linea.startsWith("TI  -")) { // Titulo
                titulo = linea.substring(6).trim();
            } else if (linea.startsWith("AU  -")) { // Autores
                autores = linea.substring(6).trim();
            } else if (linea.startsWith("AB  -")) { // Resumen
                resumen = linea.substring(6).trim();
            } else if (linea.startsWith("PY  -")) { // Año
                anio = Integer.parseInt(linea.substring(6).trim());
            } else if (linea.startsWith("TY  -")) { // Tipo de publicación
                tipo = linea.substring(6).trim();
            }

            if (linea.equals("ER  -")) { // Fin de un artículo
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
