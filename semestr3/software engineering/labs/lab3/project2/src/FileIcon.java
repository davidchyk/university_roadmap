/**
 * Leaf of the Composite: represents a file icon.
 * Uses a shared {@link IconFlyweight} to minimize memory usage.
 * Extrinsic state: file name, local position; intrinsic: shared sprite & size.
 */
public class FileIcon implements FSIcon {
    private final String fileName;
    private final IconFlyweight fw; // shared flyweight
    private int x, y;               // local position in parent directory

    /**
     * Creates a file icon with the shared FILE flyweight.
     * @param fileName display name
     */
    public FileIcon(String fileName) {
        this.fileName = fileName;
        this.fw = IconFactory.get(IconType.FILE);
    }

    @Override public String name() { return fileName; }
    @Override public int getX() { return x; }
    @Override public int getY() { return y; }
    @Override public void setPosition(int x, int y) { this.x = x; this.y = y; }

    @Override public int getWidth() { return fw.getWidth(); }
    @Override public int getHeight() { return fw.getHeight(); }

    @Override
    public void draw(int absX, int absY) {
        fw.paint(fileName, absX + x, absY + y);
    }
}
