#include <opencv2/opencv.hpp>
#include <iostream>

int main() {

    cv::Mat image = cv::imread("img/esp.png");
    if(image.empty()) {
        std::cout << "Gambar tidak ditemukan!" << std::endl;
        return -1;
    }
    cv::imshow("Display Window", image);
    cv::waitKey(0);

    return 0;
}
