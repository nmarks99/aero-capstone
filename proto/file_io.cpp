#include <iostream>
#include <fstream>
using namespace std;
int main(void) {
    
    ofstream myfile ("test.txt");
    if (myfile.is_open()){
        myfile << "This is the first line\n";
        myfile << "Here is a second line\n";
        myfile.close();
    }
    else {
        cout << "Unable to open file";
        return 0;
    }

}
