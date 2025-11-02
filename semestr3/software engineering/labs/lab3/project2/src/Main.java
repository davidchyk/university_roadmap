/**
 * Demo: filesystem icons with Composite (directories) + Flyweight (shared sprites).
 * Shows drawing to console and memory-effect (2 flyweights reused for thousands of icons).
 */
public class Main {
    public static void main(String[] args) {
        // Build a small tree
        DirectoryIcon root = new DirectoryIcon("root").setGrid(5, 6, 6);
        DirectoryIcon src  = new DirectoryIcon("src").setGrid(6, 6, 6);
        DirectoryIcon doc  = new DirectoryIcon("doc").setGrid(6, 6, 6);

        root.add(new FileIcon("README.md"));
        root.add(new FileIcon(".gitignore"));
        root.add(src);
        root.add(doc);

        src.add(new FileIcon("FSIcon.java"));
        src.add(new FileIcon("IconFlyweight.java"));
        src.add(new FileIcon("IconFactory.java"));
        src.add(new FileIcon("FileIcon.java"));
        src.add(new FileIcon("DirectoryIcon.java"));
        src.add(new FileIcon("Main.java"));

        doc.add(new FileIcon("report.tex"));
        doc.add(new FileIcon("build.xml"));
        doc.add(new FileIcon("diagram.puml"));

        // Draw tree at absolute origin (0,0)
        root.setPosition(10, 10);
        root.draw(0, 0);

        // Demonstrate memory efficiency: create many files under /src
        int extra = 5000;
        for (int i = 0; i < extra; i++) {
            src.add(new FileIcon("Generated" + i + ".java"));
        }
        System.out.println();
        System.out.printf("Children in /src: %d%n", src.getChildren().size());
        System.out.printf("Flyweights cached: %d (should be 2: FILE and FOLDER)%n",
                IconFactory.flyweightCount());

        // Draw only the /src directory header again to avoid flooding the console
        src.setPosition(10, 200);
        System.out.println("\n[Preview: redraw /src header only]");
        IconFactory.get(IconType.FOLDER).paint(src.name() + "/", src.getX(), src.getY());
        System.out.println("... (thousands of file icons share the same FILE flyweight)");
    }
}