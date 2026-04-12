public static <T> T[] add(T[] array, T element) {
    Class<?> type;
    if (array != null) {
        type = array.getClass().getComponentType();
    } else if (element != null) {
        type = element.getClass();
    } else {
        @SuppressWarnings("unchecked")
        final T[] emptyArray = (T[]) Array.newInstance(Object.class, 1);
        emptyArray[0] = element;
        return emptyArray;
    }

    int length = array == null ? 0 : Array.getLength(array);
    Object newArray = Array.newInstance(type, length + 1);
    if (array != null) {
        System.arraycopy(array, 0, newArray, 0, length);
    }
    Array.set(newArray, length, element);
    @SuppressWarnings("unchecked")
    final T[] result = (T[]) newArray;
    return result;
}