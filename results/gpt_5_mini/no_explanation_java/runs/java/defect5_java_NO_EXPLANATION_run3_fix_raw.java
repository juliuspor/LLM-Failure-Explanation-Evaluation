public static <T> T[] add(T[] array, T element) {
    Class<?> componentType = (array != null) ? array.getClass().getComponentType()
            : (element != null ? element.getClass() : Object.class);
    @SuppressWarnings("unchecked") // safe because new array will hold T elements
    T[] newArray = (T[]) copyArrayGrow1(array, componentType);
    newArray[newArray.length - 1] = element;
    return newArray;
}