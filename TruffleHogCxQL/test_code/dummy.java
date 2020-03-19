class dummy {

    // MailChimp example
    private static String mailChimpPassword1 = "0123456789abcdef0123456789abcdef-us1";
    private static String mailChimpPassword2 = "0123456789abcdef0123456789abcdef-us99";
    private static String mailChimpPassword3 = "0123456789abcdef0123456789abcdef-us06";

    private static String aSecretPasswordThatMightNotBeDetected = "abc123";
    private static String aSecret = "abc123";

    private static String url = "http://user:2282392wsddx@www.foo.com";


    // Trufflehog "Password in URL" needs username/password in URL to have the username and password
    // between 3 and 20 chars.  The path in the URL is also expected to be between 1 and 100 chars. 
    // The fixed regex will detect these.

    // Username > 20
    private static String thUrlTest1 = "http://012345678901234567890123456789:xxx@www.example.com/a/b/c/d/e/";

    // Username < 3
    private static String thUrlTest2 = "http://01:xxx@www.example.com/a/b/c/d/e/";

    // Password > 20
    private static String thUrlTest3 = "http://xxx:012345678901234567890123456789@www.example.com/a/b/c/d/e/";
    
    // Password < 3
    private static String thUrlTest4 = "http://xxx:01@www.example.com/a/b/c/d/e/";

    // Username + Password > 20
    private static String thUrlTest5 = "http://012345678901234567890123456789:012345678901234567890123456789@www.example.com/a/b/c/d/e/";

    // Username + Password < 3
    private static String thUrlTest6 = "http://xx:01@www.example.com/a/b/c/d/e/";

    // Username + Password > 20, path > 100
    private static String thUrlTest7 = "http://012345678901234567890123456789:012345678901234567890123456789@www.example.com/0123456789/0123456789/0123456789/0123456789/0123456789/0123456789/0123456789/0123456789/0123456789/0123456789";
    
    // Username + Password < 3, path > 100
    private static String thUrlTest8 = "http://xx:xx@www.example.com/0123456789/0123456789/0123456789/0123456789/0123456789/0123456789/0123456789/0123456789/0123456789/0123456789";

    // These tests simulate a stub.  The stub would depend on the "@" at the end of the string to detect.
    // Username + Password > 20, path = 0 
    private static String thUrlTest9 = "http://012345678901234567890123456789:012345678901234567890123456789@";

    // Username + Password < 3, path = 0
    private static String thUrlTest10 = "http://xx:xx@";


    private static void sendEmail(String mailKey) {

        System.out.println(mailKey);
    }

    private static void postToURL(String theUrl) {

        System.out.println(theUrl);

    }

    public static int main(String[] args) {

        sendEmail(mailChimpPassword1);

        String temp = mailChimpPassword2;

        postToURL(url);
        return 0;
    }

}