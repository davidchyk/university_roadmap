/**
 * Area calculation modes for a composite element.
 */
public enum AreaMode {
    /** Area equals the sum of all child areas. */
    SUM_CHILD_AREAS,

    /** Area equals the area of the minimal bounding box covering all children. */
    BOUNDING_BOX
}
