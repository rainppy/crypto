#include<map>
#include <iostream>
#include<NTL/ZZ.h>
#include<time.h>
using namespace std;
using namespace NTL;
ZZ shanks(ZZ a,ZZ b,ZZ n);
ZZ rho(ZZ a, ZZ b, ZZ n);
/*ZZ fx(ZZ x, ZZ a, ZZ b,ZZ n);
ZZ fa(ZZ x, ZZ a0,ZZ jie);
ZZ fb(ZZ x, ZZ b0,ZZ jie);*/
void newabx(ZZ& a, ZZ& b, ZZ& x, ZZ jie, ZZ n);
int main()
{
	ZZ p, g, t;
	p = 383;
	g = 2;
	t = 228;
	clock_t start, end;
	start = clock();
	cout << rho(g, t, p)<<endl;
	end = clock();
	cout << "耗时"<<(double)(end - start) / CLOCKS_PER_SEC <<"s"<< endl;
	p = to_ZZ("528649698299");
	g = 2;
	t = to_ZZ("149085463602");
	start = clock();
	cout << rho(g, t, p) << endl;
	end = clock();
	cout << "耗时" << (double)(end - start) / CLOCKS_PER_SEC << "s" << endl;
}
void newabx(ZZ& a, ZZ& b, ZZ& x,ZZ jie,ZZ n)
{
	int m = x % 3;
	switch (m)
	{
	case 1: 
	{x = (b * x) % n;b = (b + 1) % jie;break;}
	case 0:
	{x = (power(x, 2)) % n;a = (2 * a) % jie;b = (2 * b) % jie;break;}
	case 2:
	{x = (a * x) % n;a = (a + 1) % jie;break;}
	} 
	
}


ZZ rho(ZZ a, ZZ b, ZZ n)
{
	ZZ x1 = to_ZZ("1");
	ZZ a1 = to_ZZ("0");
	ZZ b1 = to_ZZ("0");
	ZZ X= to_ZZ("1");
	ZZ A = to_ZZ("0");
	ZZ B = to_ZZ("0");
	ZZ fail;
	fail = to_ZZ("0");
	ZZ j, gc, jie;
	jie = 0;
	for ( j = 1;j <= n;j++)
	{
		ZZ q = PowerMod(a, j, n);
		if (q == 1)
		{
			jie = j;break;
		}
	}
	cout << jie << endl;
	//阶是对的，但是此处还能加速，可不可以只判断n-1的因子
	for (int i = 0;i < n;i++)
	{
		newabx(x1, a1, b1,jie,n);
		newabx(X, A, B,jie,n);
		newabx(X, A, B,jie,n);
		cout << x1 << "  " << X<<endl;

		if (x1 == X)
		{
			ZZ r = (b1 - B) % (jie);
			if (r == 0)
				return fail;
			else
			{
				ZZ x;
				x = PowerMod(r, -1, jie );
				x = (x * (A - a1)) % jie;
				return x;
			}	
		}
	}
	return fail;
}
ZZ shanks(ZZ a, ZZ b, ZZ n)
{
	ZZ m = SqrRoot(n) + 1;
	ZZ j,i;
	map<ZZ, ZZ> hash;
	ZZ base1,base2;
	base1 = 1;
	base2 = b;
	ZZ ri, rj;
	ri = rj = 0;
	for (j = 0;j < m ;j++)
	{	
		hash[base1] = j;
		base1 = (base1 * PowerMod(a, m,n))%n;
	}
	for (i = 0;i < m;i++)
	{
		if (hash.count(base2))
		{
			rj= hash[base2];
			ri = i;
			break;
		}
		base2 = (base2 * PowerMod(a, -1, n))%n;
	}
	ZZ res;
	res = (m * rj + ri) % n;
	return res;
}