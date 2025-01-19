#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/utsname.h>

void get_latest_kernel_version(const char *repo_path, char *latest_version, size_t max_length) {
    char git_command[256];
    snprintf(git_command, sizeof(git_command), "git -C %s describe --tags `git rev-list --tags --max-count=1`", repo_path);
    FILE *fp = popen(git_command, "r");
    if (fp == NULL) {
        fprintf(stderr, "Failed to run git command\n");
        exit(EXIT_FAILURE);
    }
    fgets(latest_version, max_length, fp);
    pclose(fp);
    latest_version[strcspn(latest_version, "\n")] = '\0'; // Remove newline character
}

int main() {
    struct utsname uname_data;
    char latest_version[256];
    char repo_path[] = "/path/to/linux/repo"; // Replace with the actual path to the cloned repository

    if (uname(&uname_data) != 0) {
        perror("uname");
        exit(EXIT_FAILURE);
    }

    printf("Current kernel version: %s\n", uname_data.release);

    get_latest_kernel_version(repo_path, latest_version, sizeof(latest_version));

    if (strcmp(uname_data.release, latest_version) < 0) {
        printf("Warning: A kernel upgrade is available. Latest version is %s\n", latest_version);
    } else {
        printf("Your kernel is up to date.\n");
    }

    return 0;
}
