import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Composite: a directory icon that contains child icons (files or directories).
 * Uses a shared FOLDER flyweight for its own rendering, and lays out children.
 */
public class DirectoryIcon implements FSIcon {
    private final String dirName;
    private final IconFlyweight fw;        // shared folder sprite
    private final List<FSIcon> children = new ArrayList<>();

    // Local position of this directory within its parent
    private int x, y;

    // Simple layout parameters for children (grid-like)
    private int hGap = 8, vGap = 8; // gaps between icons
    private int cols = 6;           // columns in layout grid

    public DirectoryIcon(String dirName) {
        this.dirName = dirName;
        this.fw = IconFactory.get(IconType.FOLDER);
    }

    /** Adds a child icon; position is computed by a simple grid layout. */
    public void add(FSIcon child) {
        // place child according to current layout (cols × rows)
        int index = children.size();
        int col = index % cols;
        int row = index / cols;
        int cellW = Math.max(child.getWidth(), fw.getWidth());
        int cellH = Math.max(child.getHeight(), fw.getHeight());
        int localX = col * (cellW + hGap);
        int localY = fw.getHeight() + vGap + row * (cellH + vGap);
        child.setPosition(localX, localY);
        children.add(child);
    }

    /** Removes a child if present. */
    public void remove(FSIcon child) { children.remove(child); }

    /** @return immutable view of children */
    public List<FSIcon> getChildren() { return Collections.unmodifiableList(children); }

    /** Optional: tune layout */
    public DirectoryIcon setGrid(int columns, int hGap, int vGap) {
        if (columns >= 1) this.cols = columns;
        this.hGap = Math.max(0, hGap);
        this.vGap = Math.max(0, vGap);
        // Re-layout existing children
        for (int i = 0; i < children.size(); i++) {
            FSIcon c = children.get(i);
            int col = i % cols;
            int row = i / cols;
            int cellW = Math.max(c.getWidth(), fw.getWidth());
            int cellH = Math.max(c.getHeight(), fw.getHeight());
            int localX = col * (cellW + hGap);
            int localY = fw.getHeight() + vGap + row * (cellH + vGap);
            c.setPosition(localX, localY);
        }
        return this;
    }

    @Override public String name() { return dirName; }
    @Override public int getX() { return x; }
    @Override public int getY() { return y; }
    @Override public void setPosition(int x, int y) { this.x = x; this.y = y; }

    /** Width = max right edge of children vs own icon width. */
    @Override
    public int getWidth() {
        int maxRight = fw.getWidth();
        for (FSIcon c : children) {
            int right = c.getX() + c.getWidth();
            if (right > maxRight) maxRight = right;
        }
        return maxRight;
    }

    /** Height = own icon height + gaps + children rows height. */
    @Override
    public int getHeight() {
        if (children.isEmpty()) return fw.getHeight();
        FSIcon last = children.get(children.size() - 1);
        int bottom = last.getY() + last.getHeight();
        return Math.max(fw.getHeight(), bottom);
    }

    @Override
    public void draw(int absX, int absY) {
        // draw folder icon with label
        fw.paint(dirName + "/", absX + x, absY + y);
        // draw children relative to this directory
        int originX = absX + x;
        int originY = absY + y;
        for (FSIcon c : children) c.draw(originX, originY);
    }
}
