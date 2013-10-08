
#include <arpa/inet.h>
#include <errno.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#define CHUNKSIZE  (1024 * 1024)  /* 2^20 */
 
int server        (int   port );
int server_accept (int   ssock);
int client        (char* host, int port);

int main (int argc, char** argv)
{
  /* type, mode, host, port, size */ 
  if ( argc < 5 )
  {
    return -1;
  }

  char*  t = argv[1];
  char*  m = argv[2];
  char*  h = argv[3];
  size_t p = atoi   (argv[4]);
  size_t n = atol   (argv[5]) * CHUNKSIZE;
  char*  c = malloc (CHUNKSIZE);

  /* make sure the memory actually got allocated */
  unsigned long int i = 0;
  for ( i = 0; i < CHUNKSIZE; i++ ) {
    c[i] = '\0';
  }

  int sock = -1;

  if ( ! strcmp ("server", t) ) {
    sock = server (p);
  } else {
    sock = client (h, p);
  }


  size_t  total = 0;
  while ( total < n )
  {
    ssize_t ret = 0;

    if ( ! strcmp ("read", m) )
    {
      while ( ret <= 0 )
      {
        fprintf (stdout, ".");
        fflush  (stdout);

        ret = recv (sock, c, CHUNKSIZE, MSG_WAITALL);

        if ( ret != CHUNKSIZE )
        {
          if ( errno != EAGAIN      &&
               errno != EWOULDBLOCK )
          {
            perror ("recv failed");
            exit (-1);
          }  
        }
      }
      total += ret;
    }

    else
    {
      while ( ret <= 0 )
      {
        fprintf (stdout, ":");
        fflush  (stdout);
        
        ret = send (sock, c, CHUNKSIZE, MSG_NOSIGNAL);

        if ( ret != CHUNKSIZE )
        {
          perror ("send failed");
          exit (-1);
        }  
      }
      total += ret;
    }
  }

  close (sock);

  return 0;

}

/* -------------------------------------------------------------------------- */
int server (int port)
{
  // printf ("creating server: %d\n", port);
  /* see http://en.wikibooks.org/wiki/C_Programming/Networking_in_UNIX */
  struct sockaddr_in dest;
  struct sockaddr_in serv;
  int    ssock;

  memset (&serv, 0, sizeof (serv));
  serv.sin_family      = AF_INET;
  serv.sin_addr.s_addr = htonl (INADDR_ANY);
  serv.sin_port        = htons (port);

  ssock = socket (AF_INET, SOCK_STREAM, 0);

  /* bind serv information to ssock */
  bind (ssock, (struct sockaddr *)&serv, sizeof (struct sockaddr));

  /* start listening, allowing a queue of up to 1 pending connection */
  listen (ssock, 5);

  return server_accept (ssock);
}

int server_accept (int ssock)
{
  // printf ("server accepts\n");
  struct    sockaddr_in dest;
  socklen_t socksize = sizeof (struct sockaddr_in);

  int sock = accept (ssock, (struct sockaddr *)&dest, &socksize);

  // printf ("Incoming connection from %s\n", inet_ntoa (dest.sin_addr));

  return sock;
}


/* -------------------------------------------------------------------------- */
int client (char* host, int port)
{
  // printf ("creating client: %s %d\n", host, port);
  int                  sock;
  struct sockaddr_in   addr_server;
  struct hostent     * he_server;

  sock = socket (AF_INET, SOCK_STREAM, 0);

  if ( sock < 0 ) 
  {
    perror ("cannot open socket");
    exit (-1);
  }

  he_server = gethostbyname (host);
  if ( he_server == NULL ) 
  {
    perror ("no such host");
    exit (-1);
  }

  bzero ((char *) &addr_server, sizeof(addr_server));
  bcopy ((char *) he_server->h_addr, 
         (char *) &addr_server.sin_addr.s_addr,
                  he_server->h_length);
  addr_server.sin_family = AF_INET;
  addr_server.sin_port   = htons (port);

  if ( connect (sock, (struct sockaddr *) &addr_server, sizeof(addr_server)) < 0 )
  {
    perror ("connect failed");
    exit (-1);
  }

  return sock;
}

