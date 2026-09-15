package ua.artem;

import com.google.gson.Gson;
import java.util.Map;

public class Main {
    public static void main(String[] args) {
        Map<String, String> obj = Map.of(
                "name", "Artem",
                "lastName", "Davydchuk",
                "group", "IO-41"
        );
        String json = new Gson().toJson(obj);
        System.out.println(json);
    }
}