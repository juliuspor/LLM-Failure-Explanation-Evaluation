public Paint getPaint(double value) {
    double v = Math.max(value, this.lowerBound);
    v = Math.min(v, this.upperBound);
    // handle NaN or infinite
    if (Double.isNaN(v) || Double.isInfinite(v)) {
        v = this.lowerBound;
    }
    double range = this.upperBound - this.lowerBound;
    int g;
    if (range <= 0.0) {
        g = 0;
    }
    else {
        double frac = (v - this.lowerBound) / range;
        // ensure fraction in [0,1]
        if (frac < 0.0) {
            frac = 0.0;
        }
        else if (frac > 1.0) {
            frac = 1.0;
        }
        g = (int) Math.round(frac * 255.0);
        if (g < 0) {
            g = 0;
        }
        else if (g > 255) {
            g = 255;
        }
    }
    return new Color(g, g, g);
}