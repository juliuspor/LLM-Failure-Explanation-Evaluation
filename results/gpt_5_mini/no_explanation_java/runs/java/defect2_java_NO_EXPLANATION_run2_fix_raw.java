public java.awt.Paint getPaint(double value) {
    double v = Math.max(value, this.lowerBound);
    v = Math.min(v, this.upperBound);
    int g = (int) Math.round((v - this.lowerBound) / (this.upperBound - this.lowerBound) * 255.0);
    if (g < 0) {
        g = 0;
    } else if (g > 255) {
        g = 255;
    }
    return new Color(g, g, g);
}