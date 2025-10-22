import java.util.ArrayList;
import java.util.List;

/**
 * Composite element (group) in the {@code Composite} pattern.
 * <p>
 * Holds child elements, supports nested composites, and computes size dynamically
 * from children. Area calculation is configurable via {@link AreaMode}.
 */
public class CompositeElement implements IGameElement {
    private final String name;
    private int x, y; // local position in the parent
    private final List<IGameElement> children = new ArrayList<>();
    private AreaMode areaMode = AreaMode.SUM_CHILD_AREAS;

    /**
     * Creates a composite with a human-readable name.
     * @param name composite name
     */
    public CompositeElement(String name) { this.name = name; }

    /**
     * Sets the area calculation mode.
     * @param mode mode to use
     * @return this composite (for fluent chaining)
     */
    public CompositeElement setAreaMode(AreaMode mode) {
        this.areaMode = mode;
        return this;
    }

    /**
     * Adds a child at the given local position within this composite.
     * @param child       element to add (simple or composite)
     * @param childLocalX child local X
     * @param childLocalY child local Y
     */
    public void add(IGameElement child, int childLocalX, int childLocalY) {
        child.setPosition(childLocalX, childLocalY);
        children.add(child);
    }

    /**
     * Removes the given child if present.
     * @param child child to remove
     */
    public void remove(IGameElement child) {
        children.remove(child);
    }

    /**
     * @return internal list of children (treat as read-only)
     */
    public List<IGameElement> getChildren() { return children; }

    /** {@inheritDoc} */
    @Override public String name() { return name; }

    /** {@inheritDoc} */
    @Override public int getX() { return x; }

    /** {@inheritDoc} */
    @Override public int getY() { return y; }

    /** {@inheritDoc} */
    @Override public void setPosition(int x, int y) { this.x = x; this.y = y; }

    /**
     * Computes width as the width of the minimal bounding box enclosing all children.
     * Empty composite has width 0.
     */
    @Override
    public int getWidth() {
        if (children.isEmpty()) return 0;
        int minX = Integer.MAX_VALUE, maxX = Integer.MIN_VALUE;
        for (var c : children) {
            int left = c.getX();
            int right = c.getX() + c.getWidth();
            minX = Math.min(minX, left);
            maxX = Math.max(maxX, right);
        }
        return Math.max(0, maxX - minX);
    }

    /**
     * Computes height as the height of the minimal bounding box enclosing all children.
     * Empty composite has height 0.
     */
    @Override
    public int getHeight() {
        if (children.isEmpty()) return 0;
        int minY = Integer.MAX_VALUE, maxY = Integer.MIN_VALUE;
        for (var c : children) {
            int top = c.getY();
            int bottom = c.getY() + c.getHeight();
            minY = Math.min(minY, top);
            maxY = Math.max(maxY, bottom);
        }
        return Math.max(0, maxY - minY);
    }

    /**
     * Computes area according to {@link AreaMode}.
     * SUM_CHILD_AREAS: sum of child areas.
     * BOUNDING_BOX: getWidth() * getHeight().
     */
    @Override
    public int area() {
        if (areaMode == AreaMode.SUM_CHILD_AREAS) {
            int sum = 0;
            for (var c : children) sum += c.area();
            return sum;
        } else {
            return getWidth() * getHeight();
        }
    }

    /** {@inheritDoc} */
    @Override
    public void draw(int x, int y) {
        int absX = x + this.x;
        int absY = y + this.y;
        System.out.printf(
            "Composite.draw name=%s at=(%d,%d) size=%dx%d mode=%s children=%d%n",
            name, absX, absY, getWidth(), getHeight(), areaMode, children.size()
        );
        for (var c : children) c.draw(absX, absY);
    }
}