public static <T> T[] add(T[] array, T element) {
    Class<?> type = array != null ? array.getClass().getComponentType()
            : (element != null ? element.getClass() : Object.class);
    // TODO - this is NOT safe to ignore - see LANG-571
    @SuppressWarnings("unchecked")
    T[] newArray = (T[]) copyArrayGrow1(array, type);
    newArray[newArray.length - 1] = element;
    return newArray;
}