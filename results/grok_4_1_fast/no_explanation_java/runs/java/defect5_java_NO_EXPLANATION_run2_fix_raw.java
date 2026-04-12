private static Object copyArrayGrow1(Object array, Class<?> newArrayComponentType) {
    if (array == null) {
        return Array.newInstance(newArrayComponentType, 1);
    }
    int arrayLength = Array.getLength(array);
    Object newArray = Array.newInstance(array.getClass().getComponentType(), arrayLength + 1);
    System.arraycopy(array, 0, newArray, 0, arrayLength);
    return newArray;
}