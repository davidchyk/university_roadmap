/**
 * Demo/Client that showcases the Composite pattern implementation
 * with three scenarios required by the lab:
 * <ol>
 *   <li>single simple element;</li>
 *   <li>composite with several simple elements;</li>
 *   <li>nested composite structure (composite inside composite)
 *       and different area modes.</li>
 * </ol>
 */
public class Main {
    /**
     * Program entry point.
     * @param args unused
     */
    public static void main(String[] args) {
        // 1) Single simple element
        IGameElement hero = new SimpleElement("Hero", 2, 3);
        hero.setPosition(5, 7);
        hero.draw(0, 0);
        System.out.printf("Hero area=%d size=%dx%d%n%n", hero.area(), hero.getWidth(), hero.getHeight());

        // 2) Composite with several simple elements (area mode: SUM_CHILD_AREAS)
        CompositeElement group1 = new CompositeElement("Group1").setAreaMode(AreaMode.SUM_CHILD_AREAS);
        group1.add(new SimpleElement("Tree", 3, 4), 0, 0);
        group1.add(new SimpleElement("Rock", 2, 2), 4, 1);
        group1.add(new SimpleElement("Chest", 1, 1), 7, 0);
        group1.setPosition(10, 10);
        group1.draw(0, 0);
        System.out.printf("Group1 area=%d size=%dx%d%n%n", group1.area(), group1.getWidth(), group1.getHeight());

        // 3) Nested composite (outer uses BOUNDING_BOX, inner uses SUM_CHILD_AREAS)
        CompositeElement inner = new CompositeElement("Inner").setAreaMode(AreaMode.SUM_CHILD_AREAS);
        inner.add(new SimpleElement("Coin", 1, 1), 1, 0);
        inner.add(new SimpleElement("Key",  1, 2), 2, 2);

        CompositeElement outer = new CompositeElement("Outer").setAreaMode(AreaMode.BOUNDING_BOX);
        outer.add(new SimpleElement("Door", 2, 5), 0, 0);
        outer.add(inner, 5, 1);
        outer.setPosition(20, 3);

        outer.draw(0, 0);
        System.out.printf("Outer area(mode=%s)=%d size=%dx%d%n",
                AreaMode.BOUNDING_BOX, outer.area(), outer.getWidth(), outer.getHeight());
    }
}
