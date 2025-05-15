package archivosUtils;

import model.Producto;

import java.io.*;
import java.util.*;

public class UnificadorDeDatos {

    public void unificarDatos(List<Producto> productosCSV, List<Producto> productosRIS, List<Producto> productosBibTex) {
        Set<Producto> productosUnificados = new HashSet<>();

        // Añadir productos de cada lista
        productosUnificados.addAll(productosCSV);
        productosUnificados.addAll(productosRIS);
        productosUnificados.addAll(productosBibTex);

        // Generar los archivos de salida
        generarArchivoUnificado(productosUnificados);
        generarArchivoEliminados(productosCSV, productosRIS, productosBibTex, productosUnificados);
    }

    private void generarArchivoUnificado(Set<Producto> productosUnificados) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter("productos_unificados.txt"))) {
            for (Producto producto : productosUnificados) {
                writer.write(producto.getTitulo() + "\n");
                writer.write(producto.getAutores() + "\n");
                writer.write(producto.getResumen() + "\n");
                writer.write(producto.getAnio() + "\n");
                writer.write(producto.getTipo() + "\n");
                writer.write("\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void generarArchivoEliminados(List<Producto> productosCSV, List<Producto> productosRIS, List<Producto> productosBibTex, Set<Producto> productosUnificados) {
        Set<Producto> eliminados = new HashSet<>();
        eliminados.addAll(productosCSV);
        eliminados.addAll(productosRIS);
        eliminados.addAll(productosBibTex);

        eliminados.removeAll(productosUnificados); // Los productos eliminados son los que estaban duplicados

        try (BufferedWriter writer = new BufferedWriter(new FileWriter("productos_eliminados.txt"))) {
            for (Producto producto : eliminados) {
                writer.write(producto.getTitulo() + "\n");
                writer.write(producto.getAutores() + "\n");
                writer.write(producto.getResumen() + "\n");
                writer.write(producto.getAnio() + "\n");
                writer.write(producto.getTipo() + "\n");
                writer.write("\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
