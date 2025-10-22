/**
 * Base interface for an element of the game space.
 * <p>
 * Serves as the <b>Component</b> role in the <em>Composite</em> pattern,
 * defining a common contract for both simple and composite elements.
 */
public interface IGameElement {

    /** @return human-readable name (for logs/debugging) */
    String name();

    /** @return local X coordinate within parent composite */
    int getX();

    /** @return local Y coordinate within parent composite */
    int getY();

    /**
     * Sets the local position of this element relative to its parent composite.
     * @param x local X
     * @param y local Y
     */
    void setPosition(int x, int y);

    /**
     * Width of the element.
     * For composites, this is computed dynamically from the children's bounding box.
     * @return non-negative width
     */
    int getWidth();

    /**
     * Height of the element.
     * For composites, this is computed dynamically from the children's bounding box.
     * @return non-negative height
     */
    int getHeight();

    /**
     * Area of the element.
     * For composites, the calculation depends on {@link AreaMode}.
     * @return non-negative area
     */
    int area();

    /**
     * Demonstrational business method (drawing/logging).
     * Should print an informative line to the console.
     * @param x absolute X coordinate of the parent origin
     * @param y absolute Y coordinate of the parent origin
     */
    void draw(int x, int y);
}
