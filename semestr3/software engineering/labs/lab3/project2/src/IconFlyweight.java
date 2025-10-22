/**
 * Flyweight that stores heavy, intrinsic icon data (sprite, size, etc.).
 * In a real GUI this could hold a loaded image/texture.
 */
public final class IconFlyweight {
    private final IconType type;
    private final String spriteName;
    private final int width;
    private final int height;

    public IconFlyweight(IconType type, String spriteName, int width, int height) {
        this.type = type;
        this.spriteName = spriteName;
        this.width = width;
        this.height = height;
    }

    /** @return icon type (FILE/FOLDER) */
    public IconType getType() { return type; }

    /** @return logical sprite identifier (e.g., resource name) */
    public String getSpriteName() { return spriteName; }

    /** @return intrinsic width */
    public int getWidth() { return width; }

    /** @return intrinsic height */
    public int getHeight() { return height; }

    /**
     * Paint helper used by leaf/composite to render themselves.
     * Here we only print; in a real GUI, you'd draw an image onto Graphics.
     */
    public void paint(String label, int absX, int absY) {
        System.out.printf(
            "draw[%s sprite=%s size=%dx%d] at=(%d,%d) label=\"%s\"%n",
            type, spriteName, width, height, absX, absY, label
        );
    }
}