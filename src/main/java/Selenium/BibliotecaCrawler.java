package Selenium;

import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.io.FileWriter;
import java.io.PrintWriter;
import java.time.Duration;
import java.util.List;

public class BibliotecaCrawler {
    public static void main(String[] args) {
        System.setProperty("webdriver.chrome.driver", "C:\\Users\\USUARIO\\Documents\\DatosProgramacion\\AnalisisDeAlgoritmosProyectoFinal\\chromedriver-win64\\chromedriver.exe");

        ChromeOptions options = new ChromeOptions();

        // Prueba primero sin user-data-dir (puede causar bloqueo si el perfil está abierto)
        // String userProfile = "C:\\Users\\USUARIO\\AppData\\Local\\Google\\Chrome\\User Data";
        // options.addArguments("user-data-dir=" + userProfile);
        // options.addArguments("--profile-directory=Default");

        options.addArguments("--start-maximized");
        options.addArguments("--remote-allow-origins=*");
        options.addArguments("--disable-dev-shm-usage");
        options.addArguments("--no-sandbox");

        // Excluir la bandera enable-automation para que no se detecte automatización
        options.setExperimentalOption("excludeSwitches", new String[]{"enable-automation"});
        // NO usar useAutomationExtension, está deprecated y genera warning

        options.addArguments("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36");

        WebDriver driver = new ChromeDriver(options);
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(30));

        try {
            System.out.println("Ejecutando script...");

            // Remover navigator.webdriver para dificultar detección
            ((JavascriptExecutor) driver).executeScript("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})");

            System.out.println("Cargando página...");
            driver.get("https://library.uniquindio.edu.co/databases");

            try {
                WebElement acceptCookies = wait.until(ExpectedConditions.elementToBeClickable(By.id("onetrust-accept-btn-handler")));
                acceptCookies.click();
                System.out.println("Cookies aceptadas.");
            } catch (Exception e) {
                System.out.println("No apareció ventana de cookies.");
            }

            Thread.sleep(3000);

            WebElement basesPorFacultad = wait.until(ExpectedConditions.elementToBeClickable(By.partialLinkText("BASES DATOS")));
            basesPorFacultad.click();
            System.out.println("Clic en 'BASES DATOS x FACULTAD'.");

            Thread.sleep(1500);

            WebElement ingenieriaDiv = wait.until(ExpectedConditions.presenceOfElementLocated(
                    By.xpath("//div[@data-content-listing-item='fac-ingenier-a']")));
            ((JavascriptExecutor) driver).executeScript("arguments[0].click();", ingenieriaDiv);
            System.out.println("Click en facultad de ingeniería.");

            wait.until(ExpectedConditions.invisibilityOfElementLocated(By.className("onload-background")));

            WebElement acmLink = wait.until(ExpectedConditions.elementToBeClickable(
                    By.xpath("//span[text()='ACM Digital Library']/ancestor::a")));
            acmLink.click();

            System.out.println("Esperando carga ACM Digital Library...");
            Thread.sleep(7000);

            WebElement searchInput = wait.until(ExpectedConditions.presenceOfElementLocated(By.cssSelector("input.quick-search__input")));
            String searchText = "computational thinking";
            for (char c : searchText.toCharArray()) {
                searchInput.sendKeys(Character.toString(c));
                Thread.sleep(150);
            }
            searchInput.sendKeys(Keys.ENTER);
            System.out.println("Buscando 'computational thinking'");

            wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector("ul.rlist--inline.loa")));

            List<WebElement> authorBlocks = driver.findElements(By.cssSelector("ul.rlist--inline.loa"));

            try (PrintWriter writer = new PrintWriter(new FileWriter("autores_computational_thinking.txt"))) {
                for (WebElement block : authorBlocks) {
                    List<WebElement> authors = block.findElements(By.cssSelector("li a span"));
                    for (WebElement author : authors) {
                        String name = author.getText().trim();
                        if (!name.isEmpty()) {
                            System.out.println("Autor: " + name);
                            writer.println(name);
                        }
                    }
                }
                System.out.println("Autores guardados correctamente.");
            }

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            driver.quit();
            System.out.println("Driver cerrado.");
        }
    }
}
