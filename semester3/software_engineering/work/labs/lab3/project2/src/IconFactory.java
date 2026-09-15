import java.util.EnumMap;
import java.util.Map;

/**
 * Flyweight factory that reuses a small set of heavy icon objects.
 * Only two flyweights are created (FILE and FOLDER) and shared by all icons.
 */
public final class IconFactory {
    private static final Map<IconType, IconFlyweight> CACHE = new EnumMap<>(IconType.class);

    private IconFactory() {}

    /** Returns a shared flyweight for the given icon type. */
    public static IconFlyweight get(IconType type) {
        IconFlyweight fw = CACHE.get(type);
        if (fw == null) {
            // In real app, spriteName could be a path to PNG; size = actual image size.
            switch (type) {
                case FILE -> fw = new IconFlyweight(type, "sprite-file", 24, 24);
                case FOLDER -> fw = new IconFlyweight(type, "sprite-folder", 28, 24);
            }
            CACHE.put(type, fw);
        }
        return fw;
    }

    /** @return how many flyweights are currently cached (should be small). */
    public static int flyweightCount() {
        return CACHE.size();
    }
}
