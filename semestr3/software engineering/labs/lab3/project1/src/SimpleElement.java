/**
 * Leaf element in the {@code Composite} pattern.
 * <p>
 * Represents an indivisible game object with fixed size
 * (width × height) and a local position within its parent composite.
 */
public class SimpleElement implements IGameElement {
    private final String name;
    private int x, y;          // local position in parent
    private final int width;
    private final int height;

    /**
     * Creates a simple element with given name and size.
     * Negative width/height are clamped to zero.
     *
     * @param name   element name (for logs/debugging)
     * @param width  width (non-negative)
     * @param height height (non-negative)
     */
    public SimpleElement(String name, int width, int height) {
        this.name = name;
        this.width = Math.max(0, width);
        this.height = Math.max(0, height);
    }

    /** {@inheritDoc} */
    @Override public String name() { return name; }

    /** {@inheritDoc} */
    @Override public int getX() { return x; }

    /** {@inheritDoc} */
    @Override public int getY() { return y; }

    /** {@inheritDoc} */
    @Override public void setPosition(int x, int y) { this.x = x; this.y = y; }

    /** {@inheritDoc} */
    @Override public int getWidth() { return width; }

    /** {@inheritDoc} */
    @Override public int getHeight() { return height; }

    /** {@inheritDoc} */
    @Override public int area() { return width * height; }

    /** {@inheritDoc} */
    @Override
    public void draw(int x, int y) {
        System.out.printf("Simple.draw name=%s at=(%d,%d) size=%dx%d%n",
                name, x + this.x, y + this.y, width, height);
    }
}