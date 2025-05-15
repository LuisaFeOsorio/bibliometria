package leerDatos;

import model.Producto;

import java.io.*;
import java.util.*;

public class lectorCSV {

    public List<Producto> leerCSV(String archivo) throws IOException {
        List<Producto> productos = new ArrayList<>();
        BufferedReader br = new BufferedReader(new FileReader(archivo));
        String linea;

        while ((linea = br.readLine()) != null) {
            String[] datos = linea.split(",");
            String titulo = datos[0];
            String autores = datos[1];
            String resumen = datos[2];
            int anio = Integer.parseInt(datos[3]);
            String tipo = datos[4];

            Producto producto = new Producto(titulo, autores, resumen, anio, tipo);
            productos.add(producto);
        }

        br.close();
        return productos;
    }

}
