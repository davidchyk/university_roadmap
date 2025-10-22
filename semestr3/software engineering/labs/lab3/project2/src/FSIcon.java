/**
 * Component for file-system icons in a GUI.
 * Combines Composite (directories) + Flyweight (shared icon data).
 */
public interface FSIcon {

    /** @return display name (file or directory name) */
    String name();

    /** Local position within parent directory (for layout). */
    int getX();
    int getY();
    void setPosition(int x, int y);

    /** Width/height in pixels (or logical units). */
    int getWidth();
    int getHeight();

    /**
     * Draws the icon (demo: prints to console).
     * @param absX absolute X (parent origin + local X)
     * @param absY absolute Y (parent origin + local Y)
     */
    void draw(int absX, int absY);
}